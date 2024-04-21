import csv
import json
import urllib.request

with urllib.request.urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1') as url:
    data1 = json.loads(url.read().decode("utf-8"))

with urllib.request.urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2') as url:
    data2 = json.loads(url.read().decode("utf-8"))

with open('spot.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for item1 in data1["data"]["results"]:
        serial_no1 = item1["SERIAL_NO"] 
        for item2 in data2["data"]:
            if item2["SERIAL_NO"] == serial_no1:
                stitle = item1["stitle"]
                address = item2["address"]
                words = address.split()    
                district = words[1][0:3]
                longitude = item1["longitude"]
                latitude = item1["latitude"]
                image_url = item1["filelist"].split("https://")[1]
                writer.writerow([stitle, district, longitude, latitude, f'https://{image_url}'])