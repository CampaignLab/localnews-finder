from chalicelib.search import search
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python search_test.py <constituency> <topic>")
        return
    constituency = sys.argv[1]
    topic = sys.argv[2]
    stories = search(constituency, topic)
    for story in stories:
        print(story)


if __name__ == "__main__":
    main()
