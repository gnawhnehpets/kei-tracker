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
):
    """Return historical records for a ship by MMSI, newest first."""
    query: dict = {"MetaData.MMSI": mmsi}
    if message_type:
        if message_type not in ("PositionReport", "ShipStaticData"):
            raise HTTPException(status_code=400, detail="message_type must be PositionReport or ShipStaticData")
        query["MessageType"] = message_type

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
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$MetaData.MMSI",
            "ship_name": {"$first": "$MetaData.ShipName"},
            "last_seen": {"$first": "$timestamp"},
            "last_latitude": {"$first": "$MetaData.latitude"},
            "last_longitude": {"$first": "$MetaData.longitude"},
        }},
        {"$project": {
            "_id": 0,
            "mmsi": "$_id",
            "ship_name": 1,
            "last_seen": 1,
            "last_latitude": 1,
            "last_longitude": 1,
        }},
        {"$sort": {"last_seen": -1}},
    ]
    docs = await collection.aggregate(pipeline).to_list(length=None)
    for doc in docs:
        if isinstance(doc.get("last_seen"), datetime):
            doc["last_seen"] = doc["last_seen"].isoformat()
    return {"count": len(docs), "ships": docs}


@app.get("/health")
async def health():
    return {"status": "ok"}
