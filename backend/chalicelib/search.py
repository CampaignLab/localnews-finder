from . import stories
from . import places
import asyncio
import aiohttp


async def async_search(constituency, topic):
    print(f"Searching for {topic} stories in {constituency}")
    places_list = places.getPlaces(constituency)
    stories_list = []

    # Function to get stories for a given place
    async def get_stories_for_place(place):
        place_stories = await stories.getStories(place, topic)
        print(f"Found {len(place_stories)} stories for {place}")
        return place_stories

    async with aiohttp.ClientSession() as session:
        tasks = [get_stories_for_place(session, place) for place in places_list]
        tasks.append(get_stories_for_place(session, constituency))
        results = await asyncio.gather(*tasks)
        for result in results:
            stories_list.extend(result)

    # Filter out duplicates
    unique_stories = {story.title: story for story in stories_list}.values()

    return list(unique_stories)


def search(constituency, topic):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(async_search(constituency, topic))
    return results
