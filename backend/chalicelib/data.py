import csv


def csv_to_rows(file_path):
    data = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


towns = csv_to_rows("chalicelib/towns.csv")
media = csv_to_rows("chalicelib/media.csv")

places_map = {}
media_map = {}

for row in towns:
    key = row[0]
    places_map[key] = row[1:]

for row in media:
    media_map[row[0].replace('"', '')] = row[1]
print("The data is loaded")


def getConstituencies():
    return list(places_map.keys())


def getPlaces(constituency):
    return places_map.get(constituency, [])


def getMedia(constituency):
    return media_map.get(constituency, "")
