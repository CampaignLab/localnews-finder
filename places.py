import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("towns123.csv").sort_values(by="new_constituency_name")

places_map = {}

# Iterate through the DataFrame to populate the dictionary
for index, row in df.iterrows():
    key = row["new_constituency_name"].upper()
    value = row["town_name"]
    if pd.notna(value) and len(value) > 0:
        if key in places_map:
            places_map[key].append(value)
        else:
            places_map[key] = [value]


def getConstituencies():
    return list(places_map.keys())


def getPlaces(constituency):
    return places_map.get(constituency.upper(), [])
