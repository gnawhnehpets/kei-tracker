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

REGION_BOUNDING_BOXES = [
    [[24.0, 122.0], [46.0, 146.0]],   # Japan + surrounding waters
    [[-5.0, 95.0], [25.0, 122.0]],    # Southeast Asia / Strait of Malacca / South China Sea
]

async def collect_sample_mmsis():
    """Collect SAMPLE_COUNT unique MMSIs from Japan / Southeast Asia."""
    mmsis = set()
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": os.environ["AISSTREAM_API_KEY"],
                             "BoundingBoxes": REGION_BOUNDING_BOXES,
                             "FilterMessageTypes": ["PositionReport"]}
        await websocket.send(json.dumps(subscribe_message))
        print(f"Sampling {SAMPLE_COUNT} MMSIs from Japan / Southeast Asia...")
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
    # Known tracked ships + Japan / Southeast Asia region vessels
    hardcoded = ["257711000", "230028670", "352003002", "566524000", "431402072", "305127000", "431009418", "431005074",
                 "431602000", "477307800", "563036700", "525019017", "525100518"]

    if sample:
        mmsi_filter = await collect_sample_mmsis()
    else:
        sampled = await collect_sample_mmsis()
        # Merge hardcoded + sampled, deduplicated
        mmsi_filter = list(dict.fromkeys(hardcoded + sampled))

    print(f"Tracking MMSIs: {mmsi_filter}")

    while True:
        received_counts: dict[str, int] = {}
        try:
            async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
                subscribe_message = {"APIKey": os.environ["AISSTREAM_API_KEY"],
                                     "BoundingBoxes": REGION_BOUNDING_BOXES, #required
                                     "FiltersShipMMSI": mmsi_filter, #optional
                                     "FilterMessageTypes": ["PositionReport", "ShipStaticData"]} #optional

                await websocket.send(json.dumps(subscribe_message))
                print(f"[{datetime.now(timezone.utc)}] Connected.")

                while True:
                    try:
                        message_json = await asyncio.wait_for(websocket.recv(), timeout=RECEIVE_TIMEOUT)
                    except asyncio.TimeoutError:
                        print(f"[{datetime.now(timezone.utc)}] No message in {RECEIVE_TIMEOUT}s — reconnecting...")
                        print(f"[{datetime.now(timezone.utc)}] Messages received this session: {received_counts}")
                        break

                    message = json.loads(message_json)
                    message_type = message["MessageType"]
                    metadata = message["MetaData"]
                    timestamp = datetime.now(timezone.utc)

                    if message_type in ("PositionReport", "ShipStaticData"):
                        mmsi_str = str(metadata['MMSI'])
                        received_counts[mmsi_str] = received_counts.get(mmsi_str, 0) + 1
                        ais_message = message['Message'][message_type]
                        print(f"[{timestamp}] [{message_type}] {metadata['ShipName']} (MMSI: {metadata['MMSI']})")
                        ais_message['MessageType'] = message_type
                        ais_message['MetaData'] = metadata
                        ais_message['ship_id'] = metadata['MMSI']
                        ais_message['timestamp'] = timestamp
                        try:
                            await collection.insert_one(ais_message)
                        except Exception as db_err:
                            print(f"[{datetime.now(timezone.utc)}] DB insert error for MMSI {metadata['MMSI']}: {db_err}")

        except (websockets.ConnectionClosed, OSError) as e:
            print(f"[{datetime.now(timezone.utc)}] Connection error: {e} — reconnecting...")
            print(f"[{datetime.now(timezone.utc)}] Messages received this session: {received_counts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true",
                        help=f"Filter to {SAMPLE_COUNT} random MMSIs collected from an initial ping")
    args = parser.parse_args()
    asyncio.run(connect_ais_stream(sample=args.sample))