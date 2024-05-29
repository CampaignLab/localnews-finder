import stories
import places


def search(constituency, topic):
    places_list = places.getPlaces(constituency)
    stories_list = stories.getStories(constituency, topic)
    # TODO do this in parallel
    for place in places_list:
        stories_list.extend(stories.getStories(place, topic))
    # TODO filter out duplicates
    return stories_list


print(search("Croydon East", "crime"))
