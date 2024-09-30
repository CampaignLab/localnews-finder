from urllib.parse import unquote
from chalicelib.search import search
from chalicelib.data import getConstituencies
from chalice import Chalice, Response
from dotenv import load_dotenv
import os

load_dotenv()

app = Chalice(app_name="localnews-finder-backend")
app.lambda_function(name="localnews-finder-backend-dev").environment_variables = {
    "BING_API_KEY": os.environ["BING_API_KEY"]
}

# TODO security: specify the origins


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
