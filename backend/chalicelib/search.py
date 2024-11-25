from itertools import chain, zip_longest
from . import stories
from . import data
from .topics import TOPIC_MAP
import asyncio


# Function to get stories for a given place
async def get_stories_for_place(queue, place, term):
    place_stories = await stories.getStories(queue, place, term)
    return place_stories

async def get_stories_from_media(queue, place, term, media):
    if media == "":
        return []
    media_stories = await stories.getLocalStories(queue, place, term, media)
    return media_stories


async def async_search(constituency, topic):
    print(f"Searching for {topic} stories in {constituency}")
    places_list = data.getPlaces(constituency)
    print(f"{len(places_list)} places found: {','.join(places_list)}")
    media = data.getMedia(constituency)
    tasks = []
    tlist = list(set([topic] + TOPIC_MAP[topic]))
    queue = asyncio.Queue(maxsize=100)
    for place in places_list:
         for term in tlist:
            tasks.append(get_stories_for_place(queue, place, term))
            tasks.append(get_stories_from_media(queue, place, term, media))
    print(f"{len(tasks)} tasks created")
    results = await asyncio.gather(*tasks)
    print(f"{len(results)} results found")

    # Collate the results
    stories_list = list(chain.from_iterable(zip_longest(*results, fillvalue=None)))

    print(f"{len(stories_list)} stories found")
    # Filter out duplicates and None values
    seen_titles = set()
    unique_stories = []
    for story in stories_list:
        if story is not None and story.title not in seen_titles:
            seen_titles.add(story.title)
            unique_stories.append(story)
    print(f"{len(unique_stories)} unique stories found")
    return unique_stories


def search(constituency, topic):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(async_search(constituency, topic))
        print(f"Found {len(results)} stories")
        return results
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
            try:
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass
        loop.close()
