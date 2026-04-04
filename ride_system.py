import math
from tabulate import tabulate

# ── 1. Haversine Formula ──────────────────────────────────────
# Calculates real-world distance between two GPS coordinates (in km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return round(R * c, 2)  # returns distance in km


# ── 2. Fake Data — Drivers ────────────────────────────────────
# Each driver has: name, GPS location, passengers already onboard
drivers = [
    {"name": "Ali",     "lat": 33.6844, "lon": 73.0479, "passengers": 0, "available": True},
    {"name": "Raza",    "lat": 33.6900, "lon": 73.0550, "passengers": 2, "available": True},
    {"name": "Sara",    "lat": 33.6780, "lon": 73.0400, "passengers": 1, "available": True},
    {"name": "Bilal",   "lat": 33.7000, "lon": 73.0600, "passengers": 3, "available": True},
    {"name": "Fatima",  "lat": 33.6860, "lon": 73.0510, "passengers": 0, "available": True},
]


# ── 3. Student Ride Request ───────────────────────────────────
student = {
    "name": "Rajan",
    "pickup_lat":  33.6875,
    "pickup_lon":  73.0530,
    "drop_lat":    33.7100,
    "drop_lon":    73.0700,
}


# ── 4. Score Each Driver ──────────────────────────────────────
# Lower score = better driver
# Formula: distance_to_student + (passengers_onboard × 1.5 penalty)
def score_driver(driver, student):
    distance = haversine(
        driver["lat"], driver["lon"],
        student["pickup_lat"], student["pickup_lon"]
    )
    passenger_penalty = driver["passengers"] * 1.5
    total_score = distance + passenger_penalty
    return round(total_score, 2)


# ── 5. Find the Best Driver ───────────────────────────────────
def find_best_driver(drivers, student):
    results = []

    for driver in drivers:
        if not driver["available"]:
            continue

        distance = haversine(
            driver["lat"], driver["lon"],
            student["pickup_lat"], student["pickup_lon"]
        )
        score = score_driver(driver, student)

        results.append({
            "Driver":      driver["name"],
            "Distance km": distance,
            "Passengers":  driver["passengers"],
            "Score":       score,
        })

    # Sort by score (lowest = best)
    results.sort(key=lambda x: x["Score"])
    return results


# ── 6. Assign the Ride ────────────────────────────────────────
def assign_ride(drivers, student):
    ranked = find_best_driver(drivers, student)

    print("\n" + "="*55)
    print(f"  Ride request from: {student['name']}")
    print("="*55)

    print("\n  All available drivers ranked:\n")
    print(tabulate(ranked, headers="keys", tablefmt="rounded_outline"))

    best = ranked[0]
    print(f"\n  Best driver assigned: {best['Driver']}")
    print(f"  Distance to student:  {best['Distance km']} km")
    print(f"  Passengers onboard:   {best['Passengers']}")
    print(f"  Final score:          {best['Score']} (lower = better)")
    print(f"\n  Notification sent to {best['Driver']}:")
    print(f"  --> 'Pick up {student['name']} at ({student['pickup_lat']}, {student['pickup_lon']})'")
    print("="*55 + "\n")


# ── 7. Run it ─────────────────────────────────────────────────
assign_ride(drivers, student)