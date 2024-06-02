import stories
import places
import concurrent.futures


def search(constituency, topic):
    places_list = places.getPlaces(constituency)
    stories_list = stories.getStories(constituency, topic)

    # Function to get stories for a given place
    def get_stories_for_place(place):
        return stories.getStories(place, topic)

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


print(search("Croydon East", "crime"))
