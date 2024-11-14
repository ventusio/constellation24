from typing import Optional, Tuple

from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from pydantic import BaseModel
from shapely.geometry import Point as ShapelyPoint


class Point(BaseModel):
    lat: float
    lng: float

    def as_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lng)

    def as_geom(self) -> Geometry:
        # note: PostGIS expects (lng, lat) order
        return from_shape(ShapelyPoint(self.lng, self.lat), srid=4326)

    def from_geom(geom: Geometry):
        point: ShapelyPoint = to_shape(geom)
        return Point(lat=point.y, lng=point.x)


class Report(BaseModel):
    id: Optional[int] = None
    location: Point
    timestamp: Optional[str] = None
