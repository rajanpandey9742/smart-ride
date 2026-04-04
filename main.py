from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import math
import json

app = FastAPI(title="Smart Ride Assignment System")

# ── Connection Manager ────────────────────────────────────────
# Keeps track of all drivers currently connected via WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}  # driver_name -> websocket

    async def connect(self, driver_name: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[driver_name] = websocket
        print(f"Driver {driver_name} connected. Online drivers: {list(self.active_connections.keys())}")

    def disconnect(self, driver_name: str):
        if driver_name in self.active_connections:
            del self.active_connections[driver_name]
            print(f"Driver {driver_name} disconnected.")

    async def notify_driver(self, driver_name: str, message: dict):
        if driver_name in self.active_connections:
            ws = self.active_connections[driver_name]
            await ws.send_text(json.dumps(message))
            return True
        return False  # driver not online

    def online_drivers(self):
        return list(self.active_connections.keys())

manager = ConnectionManager()

# ── Data Models ───────────────────────────────────────────────
class RideRequest(BaseModel):
    student_name: str
    pickup_lat:   float
    pickup_lon:   float
    drop_lat:     float
    drop_lon:     float

# ── Driver Data ───────────────────────────────────────────────
drivers = [
    {"id": 1, "name": "Ali",    "lat": 33.6875, "lon": 73.0530, "passengers": 0, "available": True},
    {"id": 2, "name": "Raza",   "lat": 33.6900, "lon": 73.0550, "passengers": 2, "available": True},
    {"id": 3, "name": "Sara",   "lat": 33.6780, "lon": 73.0400, "passengers": 1, "available": True},
    {"id": 4, "name": "Bilal",  "lat": 33.7000, "lon": 73.0600, "passengers": 3, "available": True},
    {"id": 5, "name": "Fatima", "lat": 33.6860, "lon": 73.0510, "passengers": 0, "available": True},
]

# ── Haversine ─────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 2)

def score_driver(driver, request):
    distance = haversine(driver["lat"], driver["lon"], request.pickup_lat, request.pickup_lon)
    return round(distance + driver["passengers"] * 1.5, 2)

# ── Routes ────────────────────────────────────────────────────

@app.get("/")
def home():
    return {
        "message": "Smart Ride System is running!",
        "online_drivers": manager.online_drivers()
    }

@app.get("/drivers")
def get_drivers():
    return {"drivers": drivers, "online_drivers": manager.online_drivers()}

# WebSocket endpoint — drivers connect here to stay online
@app.websocket("/ws/driver/{driver_name}")
async def driver_websocket(websocket: WebSocket, driver_name: str):
    await manager.connect(driver_name, websocket)
    try:
        await websocket.send_text(json.dumps({
            "type": "connected",
            "message": f"Welcome {driver_name}! Waiting for ride assignments..."
        }))
        # Keep connection alive — listen for any messages from driver
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            # Driver can update their status
            if msg.get("type") == "status":
                for d in drivers:
                    if d["name"] == driver_name:
                        d["available"] = msg.get("available", True)
                await websocket.send_text(json.dumps({
                    "type": "status_updated",
                    "available": msg.get("available", True)
                }))
    except WebSocketDisconnect:
        manager.disconnect(driver_name)

# Ride request — assigns ride AND pushes notification to driver
@app.post("/request-ride")
async def request_ride(ride: RideRequest):
    available = [d for d in drivers if d["available"]]

    if not available:
        return {"error": "No drivers available right now"}

    ranked = sorted(available, key=lambda d: score_driver(d, ride))
    best = ranked[0]
    best_distance = haversine(best["lat"], best["lon"], ride.pickup_lat, ride.pickup_lon)
    best_score    = score_driver(best, ride)

    # Build notification message
    notification = {
        "type":        "ride_assigned",
        "student":     ride.student_name,
        "pickup_lat":  ride.pickup_lat,
        "pickup_lon":  ride.pickup_lon,
        "drop_lat":    ride.drop_lat,
        "drop_lon":    ride.drop_lon,
        "message":     f"New ride! Pick up {ride.student_name} at ({ride.pickup_lat}, {ride.pickup_lon})"
    }

    # Push to driver if they are online via WebSocket
    driver_online = await manager.notify_driver(best["name"], notification)

    all_ranked = [{
        "driver":      d["name"],
        "distance_km": haversine(d["lat"], d["lon"], ride.pickup_lat, ride.pickup_lon),
        "passengers":  d["passengers"],
        "score":       score_driver(d, ride),
    } for d in ranked]

    return {
        "student":             ride.student_name,
        "assigned_driver":     best["name"],
        "driver_notified_live": driver_online,
        "distance_km":         best_distance,
        "passengers_onboard":  best["passengers"],
        "score":               best_score,
        "all_drivers_ranked":  all_ranked,
    }