from pydantic import BaseModel
from typing import Optional
import asyncio
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
newsEndpoint = 'https://api.bing.microsoft.com/v7.0/news/search'
webEndpoint = 'https://api.bing.microsoft.com/v7.0/search'

async def do_query(session, endpoint, query):
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    params = {
            'q': query,
            'count': 5,  # Number of results
            'mkt': 'en-GB',  # Market (language)
            'safeSearch': 'Moderate'  # Safe search level
        }    
    async with session.get(endpoint, headers=headers, params=params) as response:
        if response.status == 200:
            results = await response.json()
            return results
        else:
            print(f"Error: {response.status} - {await response.text()}")
            return {}

# Rate limiting queue
async def rate_limited_query(queue, session, endpoint, query):
    await queue.put(None)  # Add a request to the queue
    try:
        response = await do_query(session, endpoint, query)
        return response
    finally:
        await asyncio.sleep(1/50)  # Wait to respect the rate limit (100 requests per second)
        queue.get_nowait()  # Remove the request from the queue


async def fetch_news(queue, session, query):
    return await rate_limited_query(queue, session, newsEndpoint, query)

async def fetch_web(queue, session, query):
    return await rate_limited_query(queue, session, webEndpoint, query)


async def getStories(queue, place, topic):
    query = f"{place} {topic}"
    async with aiohttp.ClientSession() as session:
        response = await fetch_news(queue, session, query)
        newsresults = response.get('value', [])
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
            for result in newsresults
        ]
        print(f"Found {len(retval)} stories for news {query}")
        return retval


async def getLocalStories(queue, place, term, media):
    async with aiohttp.ClientSession() as session:
        query = f"{place} {term} {media}"
        results = await fetch_web(queue, session, query)
        webpages = results.get('webPages', {}).get('value', [])
        retval = [
            Article(
                title=result["name"],
                content=result["snippet"],
                link=result["url"],
                source=result["displayUrl"],
                searchTerm=query,
                date=result.get("datePublishedDisplayText"),
            )
            for result in webpages
        ]
        print(f"Found {len(retval)} stories for web {query}")
        return retval
