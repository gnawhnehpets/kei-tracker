import asyncio
import os
import argparse
import websockets
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client[os.environ["DATABASE_NAME"]]
collection = db[os.environ["DATABASE_COLLECTION"]]

SAMPLE_COUNT = 10

async def collect_sample_mmsis():
    """Connect without MMSI filter and collect SAMPLE_COUNT unique MMSIs from the first messages."""
    mmsis = set()
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": os.environ["AISSTREAM_API_KEY"],
                             "BoundingBoxes": [[[-90, -180], [90, 180]]],
                             "FilterMessageTypes": ["PositionReport"]}
        await websocket.send(json.dumps(subscribe_message))
        print(f"Sampling {SAMPLE_COUNT} random MMSIs from initial ping...")
        async for message_json in websocket:
            message = json.loads(message_json)
            if message["MessageType"] == "PositionReport":
                mmsis.add(str(message["MetaData"]["MMSI"]))
            if len(mmsis) >= SAMPLE_COUNT:
                break
    print(f"Sampled MMSIs: {list(mmsis)}")
    return list(mmsis)

RECEIVE_TIMEOUT = 60  # seconds before assuming a dead connection

async def connect_ais_stream(sample=False):
    if sample:
        mmsi_filter = await collect_sample_mmsis()
    else:
        mmsi_filter = ["257711000", "230028670", "352003002"]

    while True:
        try:
            async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
                subscribe_message = {"APIKey": os.environ["AISSTREAM_API_KEY"],
                                     "BoundingBoxes": [[[-90, -180], [90, 180]]], #required
                                     "FiltersShipMMSI": mmsi_filter, #optional
                                     "FilterMessageTypes": ["PositionReport", "ShipStaticData"]} #optional

                await websocket.send(json.dumps(subscribe_message))
                print(f"[{datetime.now(timezone.utc)}] Connected.")

                while True:
                    try:
                        message_json = await asyncio.wait_for(websocket.recv(), timeout=RECEIVE_TIMEOUT)
                    except asyncio.TimeoutError:
                        print(f"[{datetime.now(timezone.utc)}] No message in {RECEIVE_TIMEOUT}s — reconnecting...")
                        break

                    message = json.loads(message_json)
                    message_type = message["MessageType"]
                    metadata = message["MetaData"]
                    timestamp = datetime.now(timezone.utc)

                    if message_type in ("PositionReport", "ShipStaticData"):
                        ais_message = message['Message'][message_type]
                        print(f"[{timestamp}] [{message_type}] {metadata['ShipName']} (MMSI: {metadata['MMSI']})")
                        ais_message['MessageType'] = message_type
                        ais_message['MetaData'] = metadata
                        ais_message['timestamp'] = timestamp
                        await collection.insert_one(ais_message)

        except (websockets.ConnectionClosed, OSError) as e:
            print(f"[{datetime.now(timezone.utc)}] Connection error: {e} — reconnecting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true",
                        help=f"Filter to {SAMPLE_COUNT} random MMSIs collected from an initial ping")
    args = parser.parse_args()
    asyncio.run(connect_ais_stream(sample=args.sample))