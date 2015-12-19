from . import app
from .models import HotSpots

from flask_googlemaps import Map


class Distance(object):

    def __init__(self, distance, hotspot):
        self.distance = distance
        self.name = hotspot.name
        self.location = hotspot.location
        self.latitude = hotspot.latitude
        self.longitude = hotspot.longitude

    def __cmp__(self, other):
        """
        The comparator method compares the distances properties of Distance
        objects for sorting ascending order
        """
        if other.distance < self.distance:
            return 1
        elif other.distance > self.distance:
            return -1
        else:
            return 0


def _distance_from_coordinates(lat, lon):
    """
    Makes a list of Distance objects using the distance calculated from
    the passed in latitude and longitude
    """
    distances = []
    for hotspot in HotSpots.query.all():
        distances.append(Distance(hotspot.distance((lat, lon)), hotspot))
    return distances


def generate_map(lat, lon):
    """
    Generate a map object for a given set of latitude and longtitude
    """
    distances = _distance_from_coordinates(lat, lon)
    # Sort distances in ascending order
    sorted_distances = sorted(distances)
    split_distances = sorted_distances[:2 * app.config["NUM_OF_HOTSPOTS"]]
    # Make a list of tuples containing the latitude and longitude
    ten_distances = [(e.latitude, e.longitude) for e in split_distances]
    # Remove duplicate values for the list
    ten_distances = list(set(ten_distances))

    # Build a map object using the given properties
    my_map = Map(
        identifier="hotspots",
        lat=sorted_distances[0].latitude,
        lng=sorted_distances[0].longitude,
        style="height:450px;width:450px;margin:0 auto;",
        markers=ten_distances
    )

    return my_map
