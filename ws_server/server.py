import asyncio
import websockets
import json
import time
import csv
import os

LOG_PATH = "../logs/ws_stream.csv"
os.makedirs("../logs", exist_ok=True)

# očekávaný formát dat z Questu
# { "hand": "right", "joints": { "thumb": [...], "index": [...], "middle": [...], ... } }

async def handler(websocket):
    print("[WS] Connected")
    with open(LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "hand", "joint", "x", "y", "z"])
        while True:
            try:
                msg = await websocket.recv()
                data = json.loads(msg)
                t = time.time()
                for joint, coords in data["joints"].items():
                    writer.writerow([t, data["hand"], joint, *coords])
                f.flush()
            except websockets.ConnectionClosed:
                print("[WS] Disconnected")
                break

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("[WS] Server running on ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
