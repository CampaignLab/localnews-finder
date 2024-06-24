from . import AsyncGoogleNews
from .asyncnewsapi.newsapi_client import AsyncNewsApiClient

from pydantic import BaseModel
from typing import Optional
import os
import aiohttp
import asyncio

from dotenv import load_dotenv

load_dotenv()


# TODO: neither of these is filtering by date properly, old articles are appearing

googlenews = AsyncGoogleNews.GoogleNews(lang="en", region="GB")

newsapi = AsyncNewsApiClient(os.environ["NEWS_API_KEY"])

headers = {"x-api-key": os.environ["WORLDNEWS_API_KEY"]}


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
    everything = await newsapi.get_everything(
        q=searchTerm,
        sort_by="relevancy",
        from_param="2022-07-04",
        language="en",
        page_size=10,
    )
    retval = [
        Article(
            title=article.get("title"),
            description=article.get("description"),
            content=article.get("content"),
            date=article.get("publishedAt"),
            link=article.get("url"),
            img=article.get("urlToImage"),
            source=article.get("source").get("name"),
            author=article.get("author"),
            searchTerm=searchTerm,
        )
        for article in everything.get("articles")
        if article.get("content") != "[Removed]"
    ]
    print(f"Found {len(retval)} stories on News API for {searchTerm}")
    return retval


sem = asyncio.Semaphore(1)


async def getWorldNewsApiStories(searchTerm):
    params = {
        "text": searchTerm,
        "source_countries": "gb",
        "language": "en",
        "earliest_publish_date": "2022-07-04",
        "sort": "publish-time",
        "sort_direction": "desc",
        "offset": 0,
        "number": 10,
    }
    async with sem:
        async with aiohttp.ClientSession("https://api.worldnewsapi.com") as session:
            async with session.get(
                "/search-news", params=params, headers=headers
            ) as resp:
                response = await resp.json()
                if "news" not in response:
                    print(response)
                    return []
                retval = [
                    Article(
                        title=article.get("title"),
                        description=article.get("summary"),
                        date=article.get("publish_date"),
                        link=article.get("url"),
                        img=article.get("image"),
                        author=article.get("author"),
                        searchTerm=searchTerm,
                    )
                    for article in response["news"]
                ]
                print(f"Found {len(retval)} stories on World News API for {searchTerm}")
                return retval


async def getStories(placename, topic):
    searchTerm = f"+{placename} +UK +{topic}"
    [newsresults, worldnewsresults] = await asyncio.gather(
        getNewsApiStories(searchTerm), getWorldNewsApiStories(f"{placename} {topic}")
    )
    return worldnewsresults + newsresults
