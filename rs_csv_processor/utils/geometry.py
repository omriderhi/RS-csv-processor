from typing import Tuple
import shapely


class PointLocation:
    def __init__(self, lat: float, lng: float, point: shapely.Point | None = None):
        self.lat = lat
        self.lng = lng
        self.point = point if point else shapely.Point(lat, lng)

    @classmethod
    def from_tuple(cls, coordinates: Tuple[float], lat_lng_structure: bool = True):
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

    @classmethod
    def from_point(cls, shapely_point: shapely.Point):
        return PointLocation(
            lat=shapely_point.y,
            lng=shapely_point.x,
            point=shapely_point
        )


class AreaLocation:
    def __init__(self,):
        raise NotImplementedError
