from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any


class MetaData(BaseModel):
    time_utc: str = Field(..., alias="time_utc")
    mmsi: int = Field(..., alias="mmsi")
    type: str = Field(..., alias="type")
    longitude: float = Field(..., alias="lon")
    latitude: float = Field(..., alias="lat")


class AISBaseMessage(BaseModel):
    # Common fields directly from META_DATA for convenience
    mmsi: int
    longitude: float = Field(..., alias="lon")
    latitude: float = Field(..., alias="lat")
    timestamp: str = Field(..., alias="time_utc")

    # Raw message and meta_data for deeper inspection if needed
    # message_type: Any # To hold the specific message type (e.g., Message3, Message5)
    # meta_data: MetaData

    # Pydantic configuration to allow extra fields and map aliases
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",  # Allow extra fields for now, as message types vary
    )


class AISMessage3(AISBaseMessage):
    # Fields specific to Message3
    nav_status: Optional[int] = Field(None, alias="NAV_STATUS")
    sog: Optional[float] = Field(None, alias="SOG")
    pos_accuracy: Optional[int] = Field(None, alias="POS_ACCURACY")
    cog: Optional[float] = Field(None, alias="COG")
    true_heading: Optional[int] = Field(None, alias="TRUE_HEADING")
    timestamp_field: Optional[int] = Field(
        None, alias="TIMESTAMP"
    )  # Renamed to avoid conflict with base timestamp
    spare: Optional[int] = Field(None, alias="SPARE")
    maneuver_indicator: Optional[int] = Field(None, alias="MANEUVER_INDICATOR")
    raim_flag: Optional[int] = Field(None, alias="RAIM_FLAG")
    comm_state: Optional[Any] = Field(None, alias="COMM_STATE")


class AISMessage5(AISBaseMessage):
    # Fields specific to Message5
    ais_version: Optional[int] = Field(None, alias="AIS_VERSION")
    imo: Optional[int] = Field(None, alias="IMO")
    call_sign: Optional[str] = Field(None, alias="CALL_SIGN")
    vessel_name: Optional[str] = Field(None, alias="VESSEL_NAME")
    vessel_type: Optional[int] = Field(None, alias="VESSEL_TYPE")
    dim_bow: Optional[int] = Field(None, alias="DIM_BOW")
    dim_stern: Optional[int] = Field(None, alias="DIM_STERN")
    dim_port: Optional[int] = Field(None, alias="DIM_PORT")
    dim_starboard: Optional[int] = Field(None, alias="DIM_STARBOARD")
    fix_type: Optional[int] = Field(None, alias="FIX_TYPE")
    eta_month: Optional[int] = Field(None, alias="ETA_MONTH")
    eta_day: Optional[int] = Field(None, alias="ETA_DAY")
    eta_hour: Optional[int] = Field(None, alias="ETA_HOUR")
    eta_minute: Optional[int] = Field(None, alias="ETA_MINUTE")
    draught: Optional[float] = Field(None, alias="DRAUGHT")
    destination: Optional[str] = Field(None, alias="DESTINATION")
    dte: Optional[int] = Field(None, alias="DTE")
