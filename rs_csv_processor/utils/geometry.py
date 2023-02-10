from typing import Tuple
import shapely


class PointLocation:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng
        self.point = shapely.Point(lat, lng)

    @classmethod
    def from_coords(cls, coordinates: Tuple[float], lat_lng_structure: bool = True):
        if lat_lng_structure:
            return PointLocation(
                lat=coordinates[0],
                lng=coordinates[1]
            )
        else:
            return PointLocation(
                lat=coordinates[1],
                lng=coordinates[0]
            )
