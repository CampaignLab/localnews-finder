from chalicelib.search import search

results = search("Ilford South", "NHS")
for result in results:
    print(f"'{result.searchTerm}': {result.title} {result.link}")
