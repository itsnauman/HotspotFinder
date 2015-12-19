from . import db
import math

class ZipCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, details):
        self.zipcode = details[0]
        self.latitude = float(details[1])
        self.longitude = float(details[2])

    def __repr__(self):
        return '<ZipCode %r>' % self.zipcode


class HotSpots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boro = db.Column(db.String(10))
    provider = db.Column(db.String(20))
    name = db.Column(db.String(20))
    location = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, details):
        self.boro = details[1]
        self.provider = details[3]
        self.name = details[4].decode('utf-8')
        self.location = details[5].decode('utf-8')
        self.latitude = float(details[6])
        self.longitude = float(details[7])

    def distance(self, destination):
        """
        This method implements the  Haversine Formula, it calculates the
        distances between two points on a map
        """
        lat1 = self.latitude
        lon1 = self.longitude
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        return d

    def __repr__(self):
        return '<HotSpot %r>' % self.name
