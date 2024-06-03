from flask import Flask, request, jsonify
from urllib.parse import unquote
from search import search
from places import getConstituencies

app = Flask(__name__)


@app.route("/constituencies", methods=["GET"])
def constituencies_route():
    try:
        constituencies = getConstituencies()
        return jsonify(constituencies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/search", methods=["GET"])
def search_route():
    constituency = request.args.get("constituency")
    topic = request.args.get("topic")

    if not constituency or not topic:
        return (
            jsonify({"error": "Please provide both constituency and topic parameters"}),
            400,
        )

    try:
        constituency = unquote(constituency)
        topic = unquote(topic)
        articles = search(constituency, topic)
        articles_dict = [article.model_dump() for article in articles]
        return jsonify(articles_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
