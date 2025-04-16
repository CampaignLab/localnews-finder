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
#print("The data is loaded")


def getConstituencies():
    return list(places_map.keys())


def getPlaces(constituency):
    return places_map.get(constituency, [])


def getMedia(constituency):
    return media_map.get(constituency, "")


if __name__ == "__main__":
    missing = []
    dtowns = {}
    for townlist in towns:
        for town in townlist:
            dtowns[town] = town
    for (constituency, website) in media:
        if not constituency in dtowns:
            missing.append(constituency)
            #print(f'{constituency} not mapped')
    missing = sorted(set(missing))
    #print(missing)
    for missed in missing:
        matched = False
        (first, last) = missed.split(' and ')
        #print(missed.split(' and '))
        #print(missed)
        for townlist in towns:
            for town in townlist:
                if first in town:
                    #print(','.join([missed] + townlist))
                    matched = True
        if matched:
            print(','.join([missed] + townlist))
        else:
            print(','.join(townlist))
