# Smart Ride Assignment System 🚗

## 🚀 Live Demo
API Docs: https://smart-ride-sxml.onrender.com/docs

A real-time ride assignment backend system built with Python and FastAPI.
The system automatically finds and assigns the best available driver to a 
student based on distance, current passengers, and availability — then 
instantly notifies the driver via WebSocket.

## Features

- Smart driver scoring algorithm (not just nearest — optimized)
- Real-time WebSocket notifications to drivers
- REST API with auto-generated documentation
- Haversine formula for accurate GPS distance calculation
- Live driver connection tracking

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Real-time | WebSockets |
| Algorithm | Haversine formula, custom scoring |
| Server | Uvicorn (ASGI) |
| API Docs | Swagger UI (auto-generated) |

## System Flow
Student requests ride
↓
Backend calculates Haversine distance to all active drivers
↓
Scores and ranks every driver (distance + passenger load)
↓
Assigns the best available driver
↓
Instant WebSocket push notification to driver

---

## Getting Started

### Install dependencies
```bash
pip install fastapi uvicorn websockets tabulate
```

### Start the server
```bash
uvicorn main:app --reload
```

### Connect as a driver (open a new terminal)
```bash
python driver_client.py
```

### API Documentation
Visit `http://127.0.0.1:8000/docs` for the full interactive API docs.

### Request a ride
Send a POST request to `/request-ride`:
```json
{
  "student_name": "Rajan",
  "pickup_lat": 33.6875,
  "pickup_lon": 73.0530,
  "drop_lat": 33.7100,
  "drop_lon": 73.0700
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Server status + online drivers |
| GET | `/drivers` | List all drivers |
| GET | `/drivers/nearby?lat=&lon=` | Drivers sorted by distance |
| POST | `/request-ride` | Request and assign a ride |
| WS | `/ws/driver/{name}` | Driver WebSocket connection |

---

## Project Structure
smart-ride/
├── main.py            # FastAPI backend + WebSocket server
├── driver_client.py   # Simulates a driver app connection
├── ride_system.py     # Core algorithm (Phase 1 logic)
└── README.md

---

## What I Learned

This started as a personal frustration and turned into a backend 
engineering project. I learned how REST APIs work, how to calculate 
real GPS distances using the Haversine formula, how WebSockets enable 
real-time communication, and how to think about optimization problems 
beyond the obvious solution.

The obvious solution was "pick the nearest driver."
The better solution was "pick the driver most likely to complete the ride."
