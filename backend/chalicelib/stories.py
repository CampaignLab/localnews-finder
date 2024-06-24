from . import AsyncGoogleNews
from .asyncnewsapi.newsapi_client import AsyncNewsApiClient

from pydantic import BaseModel
from typing import Optional
from urllib.parse import quote
import os

from dotenv import load_dotenv

load_dotenv()


# TODO: neither of these is filtering by date properly, old articles are appearing

googlenews = AsyncGoogleNews.GoogleNews(lang="en", region="GB")

api = AsyncNewsApiClient(os.environ["NEWS_API_KEY"])


class Article(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    img: Optional[str] = None
    author: Optional[str] = None
    searchTerm: Optional[str] = None


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
            searchTerm=searchTerm,
        )
        for result in results
    ]
    print(f"Found {len(retval)} stories on Google News for {searchTerm}")
    return retval


async def getNewsApiStories(searchTerm):
    everything = await api.get_everything(
        q=searchTerm,
        sort_by="relevancy",
        from_param="2022-07-04",
        language="en",
        page_size=10,
    )
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
            searchTerm=searchTerm,
        )
        for article in everything["articles"]
        if article["content"] != "[Removed]"
    ]
    print(f"Found {len(retval)} stories on News API for {searchTerm}")
    return retval


async def getStories(places, topic):
    placeswithquotes = [f'"{place}"' for place in places]
    orexpression = " OR ".join(placeswithquotes)
    searchTerm = quote(f'({orexpression})" AND UK AND "{topic}"')
    print(f"Search term {len(searchTerm)} long")
    newsresults = await getNewsApiStories(searchTerm)
    return newsresults
