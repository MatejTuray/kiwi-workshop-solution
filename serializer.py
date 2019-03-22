class LocationSerializer:
    """Serialize data from api for processing"""

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
        """returns referenced class property"""
        data = getattr(self, prop)
        return data
