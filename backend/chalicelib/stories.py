from pydantic import BaseModel
from typing import Optional
import os
from urllib.parse import quote
import aiohttp
import os

from dotenv import load_dotenv

load_dotenv()


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


api_key = os.environ['BING_API_KEY']
# API endpoint for Bing News Search
endpoint = 'https://api.bing.microsoft.com/v7.0/news/search'

async def fetch_news(session, query):
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    params = {
        'q': query,
        'count': 10,  # Number of results
        'mkt': 'en-GB',  # Market (language)
        'safeSearch': 'Moderate'  # Safe search level
    }

    async with session.get(endpoint, headers=headers, params=params) as response:
        if response.status == 200:
            results = await response.json()
            return results.get('value', [])
        else:
            print(f"Error: {response.status} - {await response.text()}")
            return []

async def getBingNewsStories(query):
    async with aiohttp.ClientSession() as session:
        results = await fetch_news(session, query)
        retval = [
            Article(
                title=result["name"],
                content=result["description"],
                link=result["url"],
                source=result["provider"][0]["name"],
                searchTerm=query,
                date=result["datePublished"],
                img=result["image"]["thumbnail"]["contentUrl"] if "image" in result else None,
            )
            for result in results
        ]
        print(f"Found {len(results)} results on Bing for {query}")
        return retval


async def getStories(placename, topic):
    searchTerm = f"{placename} {topic}"
    newsresults = await getBingNewsStories(searchTerm)
    return newsresults
