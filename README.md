# Smart Ride Assignment System 🚗

## The Problem That Started This

One morning I was waiting for a college ride. The nearest driver to me 
ignored my request and drove right past me. The system then assigned a 
driver who was much farther away — by the time they arrived, I was late 
to class.

That one experience made me ask: why did the nearest driver get assigned 
if they weren't going to accept it? And why doesn't the system account 
for anything other than distance?

So I built a smarter system.

---

## What This System Does Differently

Most basic ride systems just pick the nearest driver. That's it.

This system scores every available driver using a custom algorithm:
score = distance_to_student + (passengers_onboard × 1.5)

A driver 0.5 km away with 3 passengers already onboard scores 5.0.
A driver 1.2 km away with 0 passengers scores 1.2.

The emptier, more available driver wins — even if they're a little farther.
The goal is to assign the driver most likely to actually show up on time.

---

## Features

- Smart driver scoring algorithm (not just nearest — optimized)
- Real-time WebSocket notifications pushed instantly to drivers
- REST API with auto-generated documentation
- Haversine formula for accurate GPS distance on Earth's surface
- Live driver connection tracking

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Real-time | WebSockets |
| Algorithm | Haversine formula, custom scoring |
| Server | Uvicorn (ASGI) |
| API Docs | Swagger UI (auto-generated) |

---

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
