import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from bson import ObjectId

load_dotenv()

app = FastAPI(title="Kei Tracker API")

client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client[os.environ["DATABASE_NAME"]]
collection = db[os.environ["DATABASE_COLLECTION"]]


def serialize_doc(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if isinstance(doc.get("timestamp"), datetime):
        doc["timestamp"] = doc["timestamp"].isoformat()
    return doc


@app.get("/ships/{mmsi}/history")
async def get_ship_history(
    mmsi: int,
    limit: int = Query(default=100, ge=1, le=1000),
    message_type: Optional[str] = Query(default=None, description="PositionReport or ShipStaticData"),
    since: Optional[str] = Query(default=None, description="ISO 8601 timestamp — return records after this time"),
):
    """Return historical records for a ship by MMSI, newest first."""
    query: dict = {"MetaData.MMSI": mmsi}
    if message_type:
        if message_type not in ("PositionReport", "ShipStaticData"):
            raise HTTPException(status_code=400, detail="message_type must be PositionReport or ShipStaticData")
        query["MessageType"] = message_type
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="since must be a valid ISO 8601 timestamp")
        query["timestamp"] = {"$gte": since_dt}

    cursor = collection.find(query).sort("timestamp", -1).limit(limit)
    docs = [serialize_doc(doc) async for doc in cursor]

    if not docs:
        raise HTTPException(status_code=404, detail=f"No records found for MMSI {mmsi}")

    return {"mmsi": mmsi, "count": len(docs), "records": docs}


@app.get("/ships/{mmsi}/latest")
async def get_ship_latest(mmsi: int):
    """Return the most recent position report for a ship by MMSI."""
    doc = await collection.find_one(
        {"MetaData.MMSI": mmsi, "MessageType": "PositionReport"},
        sort=[("timestamp", -1)],
    )
    if not doc:
        raise HTTPException(status_code=404, detail=f"No position report found for MMSI {mmsi}")
    return serialize_doc(doc)


@app.get("/ships")
async def list_ships():
    """Return a list of unique ships seen, with their latest metadata."""
    pipeline = [
        {"$match": {"MessageType": "PositionReport"}},
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$MetaData.MMSI",
            "ship_name": {"$first": "$MetaData.ShipName"},
            "last_seen": {"$first": "$timestamp"},
            "last_latitude": {"$first": "$MetaData.latitude"},
            "last_longitude": {"$first": "$MetaData.longitude"},
            "true_heading": {"$first": "$TrueHeading"},
            "cog": {"$first": "$Cog"},
        }},
        {"$project": {
            "_id": 0,
            "mmsi": "$_id",
            "ship_name": 1,
            "last_seen": 1,
            "last_latitude": 1,
            "last_longitude": 1,
            "true_heading": 1,
            "cog": 1,
        }},
        {"$sort": {"last_seen": -1}},
    ]
    docs = await collection.aggregate(pipeline).to_list(length=None)
    for doc in docs:
        if isinstance(doc.get("last_seen"), datetime):
            doc["last_seen"] = doc["last_seen"].isoformat()

    # Fill in ship names from ShipStaticData for vessels that had no name in PositionReport metadata
    empty_name_mmsis = [doc["mmsi"] for doc in docs if not (doc.get("ship_name") or "").strip()]
    if empty_name_mmsis:
        name_cursor = collection.find(
            {
                "MetaData.MMSI": {"$in": empty_name_mmsis},
                "MessageType": "ShipStaticData",
            },
            sort=[("timestamp", -1)],
        )
        name_map: dict[int, str] = {}
        async for name_doc in name_cursor:
            mmsi_key = name_doc["MetaData"]["MMSI"]
            if mmsi_key in name_map:
                continue
            name = (name_doc.get("MetaData", {}).get("ShipName") or "").strip() or (name_doc.get("Name") or "").strip()
            if name:
                name_map[mmsi_key] = name
        for doc in docs:
            if not (doc.get("ship_name") or "").strip() and doc["mmsi"] in name_map:
                doc["ship_name"] = name_map[doc["mmsi"]]

    return {"count": len(docs), "ships": docs}


@app.get("/health")
async def health():
    return {"status": "ok"}
