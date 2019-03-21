import requests
import sys
import pandas
import os

r = requests.get("https://api.skypicker.com/locations?type=box&low_lat=49.890401610&low_lon=-6.151319&high_lat=61.2520"
                 "17&high_lon=-0.321528&locale=en-US&location_types=airport&limit=500&sort=name&active_only=true")
json = r.json()
data = json["locations"]
clean_data = []

class LocationSerializer:
    def __init__(self, iata, names, icao, lat, lon, cities):
        self.iata = iata
        self.names = names
        self.icao = icao
        self.lat = str(lat)
        self.lon = str(lon)
        self.coords = F"{self.lat},{self.lon}"
        self.cities = cities
        self.row = [self.iata, self.names, self.icao, self.lat, self.lon, self.cities]
    def return_prop(self, prop):
        data = getattr(self, prop);
        return data;

for loc in data:
    serializer = LocationSerializer(loc["id"], loc["name"], loc["icao"], loc["location"]["lat"],
                                    loc["location"]["lon"],loc["city"]["name"])
    clean_data.append(serializer)

def write_excel_dump(rows, headers):
    #
    # Export data to excel file, openpyxl required
    #
    df = pandas.DataFrame(rows, columns=headers)
    print(df)
    df.to_excel("output.xlsx")
    print_separator()
    print("\n")
    print(F"Excel file saved in {os.path.dirname(os.path.abspath(__file__))}")

def print_separator():
    print("----------------------------------------------------------------------------------------")

if len(sys.argv) == 2 and sys.argv[1] == "--full":
    #
    # Dump entire list of serializers
    #
    rows = []
    for el in clean_data:
            rows.append(el.row)
    print_separator()
    write_excel_dump(rows, ["iata", "name", "icao", "lat", "lon", "city_name"]);

elif len(sys.argv) == 2 and sys.argv[1] == "--help":
    #
    # Show help
    #
    print_separator()
    print("Ways how to run the program\n")
    print("You can specify multiple options in the program:\n")
    print("--help - print help message")
    print("--cities - cities with airports")
    print("--coords - coordinates of each airport")
    print("--iata - IATA codes")
    print("--names - name of the airport")
    print("--icao - ICAO codes")
    print("--lat - latitude as a separate column")
    print("--lon - latitude as a separate column")
    print("--full - print every detail from each airport\n")
    print("You can mix and match cmd line arguments to create your own table")  
    print("When run without any option, only name and IATA code of airport is provided")

elif len(sys.argv) >= 2 and ("--full" or "--help") not in sys.argv:
    #
    # Display & output cols by single or multiple args
    # if wrong args are provided (full / help)
    # else block is executed
    #
    rows = []
    headers = []
    for i in range(1, len(sys.argv)):
        headers.append(sys.argv[i].replace("--", ""))
    for el in clean_data:
        helper = []
        for j in headers:
            helper.append(el.return_prop(sys.argv[headers.index(j) + 1].replace("--", "")))
        rows.append(helper)
    print_separator()
    write_excel_dump(rows, headers)

else:
    #
    # Default - return name and iata code of airport
    #
    rows = []
    headers = ["iata", "name"]
    for el in clean_data:
        rows.append([el.iata, el.names])
    print_separator()
    write_excel_dump(rows, headers);
