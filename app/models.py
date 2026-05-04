from pydantic import BaseModel

class Position(BaseModel):
    lat: float
    lon: float

class Status(BaseModel):
    distance_m: float
    bearing_deg: float
    trend: str

