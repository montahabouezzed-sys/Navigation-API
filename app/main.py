
from fastapi import FastAPI, HTTPException
"""from models import Position, Status
from logic import haversine, bearing, trend
import state"""
from app.models import Position, Status
from app.logic import haversine, bearing, trend
from app import state

app = FastAPI(title="Navigation Guidance API")

@app.post("/set_destination")
def set_destination(pos: Position):
    state.destination = pos
    state.last_distance = None
    return {"message": "Destination set."}

@app.post("/update_position", response_model=Status)
def update_position(pos: Position):
    if state.destination is None:
        raise HTTPException(status_code=400, detail="Destination not set.")

    dest = state.destination
    dist = haversine(pos.lat, pos.lon, dest.lat, dest.lon)
    brng = bearing(pos.lat, pos.lon, dest.lat, dest.lon)
    tr = trend(dist, state.last_distance)

    state.last_distance = dist

    return Status(distance_m=dist, bearing_deg=brng, trend=tr)

@app.get("/status", response_model=Status)
def get_status():
    if state.destination is None or state.last_distance is None:
        raise HTTPException(status_code=400, detail="No position updates yet.")
    dest = state.destination
    return Status(
        distance_m=state.last_distance,
        bearing_deg=bearing(0,0,0,0),  # placeholder
        trend="unknown"
    )
