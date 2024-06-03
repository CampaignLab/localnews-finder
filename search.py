import stories
import places
import concurrent.futures


def search(constituency, topic):
    print(f"Searching for {topic} stories in {constituency}")
    places_list = places.getPlaces(constituency)
    stories_list = stories.getStories(constituency, topic)
    print(f"Found {len(stories_list)} stories in {constituency}")

    # Function to get stories for a given place
    def get_stories_for_place(place):
        place_stories = stories.getStories(place, topic)
        print(f"Found {len(place_stories)} stories for {place}")
        return place_stories

    # Use ThreadPoolExecutor to parallelize the fetching of stories
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_stories_for_place, place) for place in places_list
        ]
        for future in concurrent.futures.as_completed(futures):
            stories_list.extend(future.result())

    # Filter out duplicates
    unique_stories = {story.title: story for story in stories_list}.values()

    return list(unique_stories)
