import csv


def csv_to_dict(file_path):
    data = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def tsv_to_dict(file_path):
    data = []
    with open(file_path, mode="r") as tsv_file:
        tsv_reader = csv.DictReader(tsv_file, delimiter="\t")
        for row in tsv_reader:
            data.append(row)
    return data


towns = csv_to_dict("chalicelib/towns123.csv")

places_map = {}

for row in towns:
    key = row["new_constituency_name"]
    value = row["town_name"]
    if len(value) > 0:
        if key in places_map:
            places_map[key].append(value)
        else:
            places_map[key] = [value]
print("The data is loaded")


def getConstituencies():
    return list(places_map.keys())


def getPlaces(constituency):
    return [constituency] + places_map.get(constituency, [])
