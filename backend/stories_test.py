from chalicelib.stories import getStories

import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python stories_test.py <placename> <topic>")
        return
    placename = sys.argv[1]
    topic = sys.argv[2]
    stories = getStories(placename, topic)
    for story in stories:
        print(story)


if __name__ == "__main__":
    main()
