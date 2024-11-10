from typing import Tuple

from pydantic import BaseModel


class Point(BaseModel):
    lat: float
    lng: float

    def as_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lng)
