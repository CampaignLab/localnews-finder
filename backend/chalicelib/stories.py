from . import AsyncGoogleNews
from .asyncnewsapi.newsapi_client import AsyncNewsApiClient
from pydantic import BaseModel
from typing import Optional
import asyncio

# TODO: neither of these is filtering by date properly, old articles are appearing

googlenews = AsyncGoogleNews.GoogleNews(lang="en", region="GB")

api = AsyncNewsApiClient(api_key="d3f8935cccc84a7a8e7e30c14d47c673")


class Article(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    img: Optional[str] = None
    author: Optional[str] = None


async def getGoogleNewsStories(searchTerm):
    googlenews.clear()
    results = await googlenews.get_news(searchTerm)
    retval = [
        Article(
            title=result["title"],
            date=result["date"],
            link=result["link"],
            img=result["img"],
            source=result["media"],
            author=result["reporter"],
        )
        for result in results
    ]
    print(f"Found {len(retval)} stories on Google News for {searchTerm}")
    return retval


async def getNewsApiStories(searchTerm):
    everything = await api.get_everything(q=searchTerm)
    retval = [
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
        for article in everything["articles"]
    ]
    print(f"Found {len(retval)} stories on News API for {searchTerm}")
    return retval


async def getStories(placename, topic):
    searchTerm = f"{placename} {topic}"
    newsresults, googleresults = await asyncio.gather(
        getNewsApiStories(searchTerm), getGoogleNewsStories(searchTerm)
    )
    return newsresults + googleresults
