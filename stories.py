from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

googlenews = GoogleNews(lang="en", region="GB", start="04/01/2020", encode="utf-8")

api = NewsApiClient(api_key="d3f8935cccc84a7a8e7e30c14d47c673")


class Article(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    img: Optional[str] = None
    author: Optional[str] = None


def getGoogleNewsStories(searchTerm):
    googlenews.clear()
    googlenews.get_news(searchTerm)
    return [
        Article(
            title=result["title"],
            date=result["date"],
            link=result["link"],
            img=result["img"],
            source=result["media"],
            author=result["reporter"],
        )
        for result in googlenews.results()
    ]


def getNewsApiStories(searchTerm):
    return [
        Article(
            title=article["title"],
            description=article["description"],
            content=article["content"],
            date=article["publishedAt"],
            link=article["url"],
            img=article["urlToImage"],
            source=article["source"]["name"],
            author=article["author"],
        )
        for article in api.get_everything(q=searchTerm)["articles"]
    ]


def getStories(placename, topic):
    searchTerm = f"{placename} {topic}"
    return getNewsApiStories(searchTerm) + getGoogleNewsStories(searchTerm)
