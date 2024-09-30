from chalicelib.search import search

results = search("Croydon East", "NHS")
for result in results:
    print(f"'{result.searchTerm}': {result.title} ({result.category}) {result.link}")
