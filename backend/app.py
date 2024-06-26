from urllib.parse import unquote
from chalicelib.search import search
from chalicelib.data import getConstituencies
from chalice import Chalice, Response
from dotenv import load_dotenv
import os
import json
from redis import Redis
import aiohttp
import asyncio


load_dotenv()

app = Chalice(app_name="localnews-finder-backend")
app.lambda_function(name="localnews-finder-backend-dev").environment_variables = {
    "NEWS_API_KEY": os.environ["NEWS_API_KEY"],
}

# Create a boto3 client for Lambda
# lambda_client = boto3.client("lambda")

redis = Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])


@app.route("/constituencies", methods=["GET"], cors=True)
def constituencies_route():
    try:
        constituencies = getConstituencies()
        return constituencies
    except Exception as e:
        return Response(status_code=500, body={"error": str(e)})


@app.route("/search", methods=["GET"], cors=True)
def search_route():
    query = app.current_request.query_params
    constituency = query["constituency"]
    topic = query["topic"]
    doSearch(constituency, topic)


@app.lambda_function(name="search-async")
def search_async(event, context):
    # This is the target lambda function
    print("Event received: ", event)
    constituency = event.get("constituency")
    topic = event.get("topic")

    try:
        doSearch(constituency, topic)
    except Exception as e:
        print("Error: ", e)


def doSearch(constituency, topic):
    if not constituency or not topic:
        return Response(
            status_code=400,
            body={"error": "Please provide both constituency and topic parameters"},
        )

    try:
        print(f"fetching results {constituency} and {topic}")
        constituency = unquote(constituency)
        topic = unquote(topic)
        articles = search(constituency, topic)
        articles_dict = [article.model_dump() for article in articles]
        return articles_dict
    except Exception as e:
        return Response(status_code=500, body={"error": str(e)})


@app.route("/search2", methods=["POST"], cors=True)
def postSearch():
    request = app.current_request
    data = request.json_body

    constituency = unquote(data.get("constituency"))
    topic = unquote(data.get("topic"))
    if not constituency or not topic:
        return Response(
            status_code=400,
            body={"error": "Please provide both constituency and topic parameters"},
        )
    status = redis.get(f"{constituency}-{topic}-status")

    if status and status == "ready":
        articles = check_redis(constituency, topic)
        if articles:
            return articles

    if status and status == "processing":
        return Response(
            status_code=204, body={"not ready": "Search results not yet ready"}
        )

    # Invoke the target lambda asynchronously
    redis.set(f"{constituency}-{topic}-status", "processing")
    asyncio.run(call_lambda())
    # parameters = {"constituency": constituency, "topic": topic}
    # lambda_client.invoke(
    #     FunctionName="localnews-finder-backend-dev-search-async",
    #     InvocationType="Event",  # Asynchronous invocation
    #     Payload=json.dumps(parameters).encode("utf-8"),
    # )
    # Return immediately without waiting for the target lambda
    return Response(
        body={"status": "Search initiated"},
        status_code=202,
        headers={"Content-Type": "application/json"},
    )


async def call_lambda(constituency, topic):
    async with aiohttp.ClientSession() as session:
        doSearch(constituency, topic)


def check_redis(constituency, topic):
    articles = redis.lrange(f"{constituency}-{topic}-data", 0, -1)
    if articles:
        return json.loads(articles)
    else:
        return None
