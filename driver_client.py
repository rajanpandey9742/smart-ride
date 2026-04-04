import asyncio
import websockets
import json

DRIVER_NAME = "Ali"  # Change this to test different drivers

async def connect_as_driver():
    url = f"ws://127.0.0.1:8000/ws/driver/{DRIVER_NAME}"
    print(f"Connecting as driver: {DRIVER_NAME}...")

    async with websockets.connect(url) as ws:
        print(f"Connected! Listening for ride assignments...\n")

        while True:
            message = await ws.recv()
            data = json.loads(message)

            if data["type"] == "connected":
                print(f"Server: {data['message']}\n")

            elif data["type"] == "ride_assigned":
                print("=" * 45)
                print("  NEW RIDE ASSIGNED!")
                print("=" * 45)
                print(f"  Student:    {data['student']}")
                print(f"  Pickup:     ({data['pickup_lat']}, {data['pickup_lon']})")
                print(f"  Drop-off:   ({data['drop_lat']}, {data['drop_lon']})")
                print(f"  Message:    {data['message']}")
                print("=" * 45 + "\n")

asyncio.run(connect_as_driver())