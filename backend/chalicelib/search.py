from . import stories
from . import data
import asyncio


# Function to get stories for a given place
async def get_stories_for_place(place, term):
    place_stories = await stories.getStories(place, term)
    return place_stories


async def async_search(constituency, topic):
    print(f"Searching for {topic} stories in {constituency}")
    places_list = data.getPlaces(constituency)
    print(f"{len(places_list)} places found")

    tasks = []
    for place in places_list:
        tasks.append(get_stories_for_place(place, topic))
    print(f"{len(tasks)} tasks created")
    results = await asyncio.gather(*tasks)
    stories_list = []
    for result in results:
        stories_list.extend(result)

    # Filter out duplicates
    unique_stories = {story.title: story for story in stories_list}.values()

    return list(unique_stories)


def search(constituency, topic):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(async_search(constituency, topic))
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
