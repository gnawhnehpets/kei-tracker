from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any


class CommState(BaseModel):
    SYNC_STATE: int
    SLOT_TIMEOUT: int
    RECEIVE_SLOTS: int


class AISMessage3(BaseModel):
    MMSI: int
    NAV_STATUS: int
    SOG: float
    POS_ACCURACY: int
    LONGITUDE: float = Field(alias="LONGITUDE")
    LATITUDE: float = Field(alias="LATITUDE")
    COG: float
    TRUE_HEADING: int
    TIMESTAMP: int
    SPARE: int
    MANEUVER_INDICATOR: int
    RAIM_FLAG: int
    COMM_STATE: CommState


class AISMessage5(BaseModel):
    MMSI: int
    IMONumber: Optional[int] = None
    CallSign: Optional[str] = None
    VesselName: Optional[str] = None
    VesselType: Optional[int] = None
    Length: Optional[int] = None
    Breadth: Optional[int] = None
    FixDevice: Optional[int] = None
    ETA: Optional[str] = None
    Draught: Optional[float] = None
    Destination: Optional[str] = None


class MetaData(BaseModel):
    time_utc: str
    mmsi: int
    type: str
    lon: float
    lat: float


class AISMessage(BaseModel):
    Message: Dict[str, Any]
    MetaData: MetaData
