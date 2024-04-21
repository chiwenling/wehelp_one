import urllib.request
import json
import csv

with urllib.request.urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1') as url:
    data1 = json.loads(url.read().decode("utf-8"))

with urllib.request.urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2') as url:
    data2 = json.loads(url.read().decode("utf-8"))

attraction_dict = {}
for item1 in data1["data"]["results"]:
    attraction_dict[item1["SERIAL_NO"]] = item1["stitle"]

stationName = {}
for item2 in data2["data"]:
    mrt_station = item2.get("MRT")
    if mrt_station:
        attraction = attraction_dict.get(item2['SERIAL_NO'], 'N/A')
        if mrt_station not in stationName:
            stationName[mrt_station] = []
        if attraction not in stationName[mrt_station]:
             stationName[mrt_station].append(attraction)

with open('mrt.csv', 'w', newline='', encoding='utf-8') as csvfile:
    for mrt_station, attractions in stationName.items():
        attractions_str = ", ".join(attractions)
        csvfile.write(f"{mrt_station}, {attractions_str}\n")