import requests

from serializer import LocationSerializer

clean_data = []
url = "https://api.skypicker.com/locations?type=box&low_lat=49.890401610&low_lon=-6.151319&high_lat=61.252017&" \
      "high_lon=-0.321528&locale=en-US&location_types=airport&limit=500&sort=name&active_only=true"
r = requests.get(url)
json = r.json()["locations"]

for loc in json:
    serializer = LocationSerializer(loc["id"], loc["name"], loc["icao"], loc["location"]["lat"],
                                    loc["location"]["lon"], loc["city"]["name"])
    clean_data.append(serializer)
