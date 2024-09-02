from urllib.parse import unquote
from chalicelib.search import search
from chalice import Chalice, Response
from dotenv import load_dotenv
import os
import json
from redis import Redis
import aiohttp
import asyncio
import boto3


load_dotenv()

app = Chalice(app_name="localnews-finder-backend")

# Create a boto3 client for Lambda

lambda_client = boto3.client("lambda") if os.environ["RUN_LAMBDA"] == True else None

redis = Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])


@app.route("/search", methods=["POST"], cors=True)
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
    redis.set(f"{constituency}-{topic}-status", "processing")

    # Invoke the target lambda asynchronously
    asyncio.run(call_lambda(constituency, topic))
    # Return immediately without waiting for the target lambda
    return Response(
        body={"status": "Search initiated"},
        status_code=202,
        headers={"Content-Type": "application/json"},
    )


def check_redis(constituency, topic):
    articles = redis.lrange(f"{constituency}-{topic}-data", 0, -1)
    if articles:
        return json.loads(articles)
    else:
        return None


async def call_lambda(constituency, topic):
    if os.environ["RUN_LAMBDA"] == True:
        parameters = {"constituency": constituency, "topic": topic}
        await lambda_client.invoke(
            FunctionName="localnews-finder-backend-dev-search-async",
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps(parameters).encode("utf-8"),
        )
    else:
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
    try:
        print(f"fetching results {constituency} and {topic}")
        constituency = unquote(constituency)
        topic = unquote(topic)
        articles = search(constituency, topic)
        articles_dict = [article.model_dump() for article in articles]
        return articles_dict
    except Exception as e:
        return Response(status_code=500, body={"error": str(e)})
