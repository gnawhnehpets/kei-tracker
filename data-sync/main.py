import asyncio
import os
import httpx
from datetime import datetime, timezone
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client[os.environ["DATABASE_NAME"]]
collection = db[os.environ["DATABASE_COLLECTION"]]

BASE_URL = "https://api.marinesia.com/api/v2/vessel/location/latest"
POLL_INTERVAL = 1800  # seconds between full poll cycles
REQUEST_DELAY = 2     # seconds between individual MMSI requests

MMSI_LIST = ["257711000"]


async def poll_marinesia(mmsi_list: list[str]):
    api_key = os.environ["MARINESIA_API_KEY"]

    async with httpx.AsyncClient(timeout=15) as http:
        while True:
            received_counts: dict[str, int] = {}
            for mmsi in mmsi_list:
                timestamp = datetime.now(timezone.utc)
                try:
                    resp = await http.get(
                        BASE_URL,
                        params={"mmsi": mmsi, "key": api_key},
                    )
                    resp.raise_for_status()
                    body = resp.json()
                except httpx.HTTPStatusError as e:
                    print(f"[{timestamp}] HTTP error {e.response.status_code} for MMSI {mmsi}: {e.response.text}")
                    await asyncio.sleep(REQUEST_DELAY)
                    continue
                except Exception as e:
                    print(f"[{timestamp}] Request error for MMSI {mmsi}: {e}")
                    await asyncio.sleep(REQUEST_DELAY)
                    continue

                if body.get("error"):
                    print(f"[{timestamp}] API error for MMSI {mmsi}: {body.get('message')}")
                    await asyncio.sleep(REQUEST_DELAY)
                    continue

                vessel = body.get("data")
                if not vessel:
                    print(f"[{timestamp}] No data for MMSI {mmsi}")
                    await asyncio.sleep(REQUEST_DELAY)
                    continue

                mmsi_str = str(vessel.get("mmsi", mmsi))
                received_counts[mmsi_str] = received_counts.get(mmsi_str, 0) + 1

                doc = {
                    # Normalized to aisstream PascalCase field names
                    "Cog":                      vessel.get("cog"),
                    "CommunicationState":        vessel.get("com_state"),
                    "Latitude":                  vessel.get("lat"),
                    "Longitude":                 vessel.get("lng"),
                    "NavigationalStatus":        vessel.get("status"),
                    "PositionAccuracy":          vessel.get("pos_acc"),
                    "Raim":                      vessel.get("raim"),
                    "RateOfTurn":                vessel.get("rot"),
                    "RepeatIndicator":           vessel.get("repeat"),
                    "Sog":                       vessel.get("sog"),
                    "Spare":                     vessel.get("spare"),
                    "SpecialManoeuvreIndicator": vessel.get("smi"),
                    "TrueHeading":               vessel.get("hdt"),
                    "UserID":                    vessel.get("mmsi"),
                    "Valid":                     vessel.get("valid"),
                    # Marinesia-only extras
                    "imo":     vessel.get("imo"),
                    "dest":    vessel.get("dest"),
                    "eta":     vessel.get("eta"),
                    "draught": vessel.get("draught"),
                    "ts":      vessel.get("ts"),
                    # Shared envelope fields
                    "MessageType": "PositionReport",
                    "MetaData": {
                        "MMSI":        vessel.get("mmsi"),
                        "MMSI_String": mmsi_str,
                        "ShipName":    "",
                        "latitude":    vessel.get("lat"),
                        "longitude":   vessel.get("lng"),
                        "time_utc":    vessel.get("ts"),
                    },
                    "ship_id":   vessel.get("mmsi"),
                    "timestamp": timestamp,
                }
                print(f"[{timestamp}] [PositionReport] MMSI: {mmsi_str} "
                      f"lat={vessel.get('lat')} lng={vessel.get('lng')} "
                      f"sog={vessel.get('sog')} cog={vessel.get('cog')}")
                try:
                    await collection.insert_one(doc)
                except Exception as db_err:
                    print(f"[{timestamp}] DB insert error for MMSI {mmsi_str}: {db_err}")

                await asyncio.sleep(REQUEST_DELAY)

            print(f"[{datetime.now(timezone.utc)}] Poll complete. Counts this cycle: {received_counts}. "
                  f"Sleeping {POLL_INTERVAL}s...")
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(poll_marinesia(MMSI_LIST))
    # asyncio.run(connect_ais_stream(sample=args.sample, mmsi=args.mmsi))