import pytest
import os
import sys
from pydantic import ValidationError

# Add data-sync/src to sys.path for module discovery
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

# Sample AIS Message Data (simplified based on plan's reference)
sample_message_3_json = {
    "MESSAGE_TYPE": {
        "Message3": {
            "MMSI": 123456789,
            "NAV_STATUS": 0,
            "SOG": 10.5,
            "POS_ACCURACY": 1,
            "LONGITUDE": -70.1234,
            "LATITUDE": 40.5678,
            "COG": 120.0,
            "TRUE_HEADING": 115,
            "TIMESTAMP": 1678886400,
            "SPARE": 0,
            "MANEUVER_INDICATOR": 0,
            "RAIM_FLAG": 0,
            "COMM_STATE": {},
        }
    },
    "META_DATA": {
        "time_utc": "2023-03-15T12:00:00Z",
        "mmsi": 123456789,
        "type": "AISMessage",
        "lon": -70.1234,
        "lat": 40.5678,
    },
}

sample_message_5_json = {
    "MESSAGE_TYPE": {
        "Message5": {
            "MMSI": 123456789,
            "AIS_VERSION": 2,
            "IMO": 9876543,
            "CALL_SIGN": "ABC1234",
            "VESSEL_NAME": "EXAMPLE SHIP",
            "VESSEL_TYPE": 70,
            "DIM_BOW": 10,
            "DIM_STERN": 100,
            "DIM_PORT": 5,
            "DIM_STARBOARD": 15,
            "FIX_TYPE": 1,
            "ETA_MONTH": 3,
            "ETA_DAY": 15,
            "ETA_HOUR": 10,
            "ETA_MINUTE": 30,
            "DRAUGHT": 12.5,
            "DESTINATION": "SOME PORT",
            "DTE": 0,
        }
    },
    "META_DATA": {
        "time_utc": "2023-03-15T12:00:00Z",
        "mmsi": 123456789,
        "type": "AISMessage",
        "lon": -70.1234,
        "lat": 40.5678,
    },
}


@pytest.fixture
def ais_models():
    from models.ais import AISBaseMessage, AISMessage3, AISMessage5

    return AISBaseMessage, AISMessage3, AISMessage5


def test_ais_base_message_validates_common_fields(ais_models):
    AISBaseMessage, _, _ = ais_models
    meta_data = sample_message_3_json["META_DATA"]
    base_message = AISBaseMessage(**meta_data)

    assert base_message.mmsi == meta_data["mmsi"]
    assert base_message.longitude == meta_data["lon"]
    assert base_message.latitude == meta_data["lat"]
    assert base_message.timestamp == meta_data["time_utc"]


def test_ais_message_3_validates_sample_data(ais_models):
    _, AISMessage3, _ = ais_models
    message_3_data = sample_message_3_json["MESSAGE_TYPE"]["Message3"]
    meta_data = sample_message_3_json["META_DATA"]

    # Combine message and meta data for the model
    combined_data = {**message_3_data, **meta_data}
    ais_message_3 = AISMessage3(**combined_data)

    assert ais_message_3.mmsi == message_3_data["MMSI"]
    assert ais_message_3.sog == message_3_data["SOG"]
    assert ais_message_3.longitude == message_3_data["LONGITUDE"]
    assert ais_message_3.latitude == message_3_data["LATITUDE"]
    assert ais_message_3.timestamp == meta_data["time_utc"]


def test_ais_message_5_validates_sample_data(ais_models):
    _, _, AISMessage5 = ais_models
    message_5_data = sample_message_5_json["MESSAGE_TYPE"]["Message5"]
    meta_data = sample_message_5_json["META_DATA"]

    # Combine message and meta data for the model
    combined_data = {**message_5_data, **meta_data}
    ais_message_5 = AISMessage5(**combined_data)

    assert ais_message_5.mmsi == message_5_data["MMSI"]
    assert ais_message_5.vessel_name == message_5_data["VESSEL_NAME"]
    assert ais_message_5.imo == message_5_data["IMO"]
    assert ais_message_5.destination == message_5_data["DESTINATION"]
    assert ais_message_5.timestamp == meta_data["time_utc"]


def test_ais_message_invalid_input_raises_validation_error(ais_models):
    AISBaseMessage, AISMessage3, AISMessage5 = ais_models

    # Test AISBaseMessage with missing required field
    invalid_meta_data = {"mmsi": 123456789, "lon": -70.1234, "lat": 40.5678}
    with pytest.raises(ValidationError):
        AISBaseMessage(**invalid_meta_data)

    # Test AISMessage3 with missing required field (e.g., MMSI)
    invalid_message_3_data = {
        "SOG": 10.5,
        "LONGITUDE": -70.1234,
        "LATITUDE": 40.5678,
        "time_utc": "2023-03-15T12:00:00Z",
    }
    with pytest.raises(ValidationError):
        AISMessage3(**invalid_message_3_data)

    # Test AISMessage5 with invalid data type for a field (e.g., MMSI as string)
    invalid_message_5_data = {
        "MMSI": "invalid",
        "AIS_VERSION": 2,
        "IMO": 9876543,
        "VESSEL_NAME": "EXAMPLE SHIP",
        "time_utc": "2023-03-15T12:00:00Z",
        "lon": -70.1234,
        "lat": 40.5678,
    }
    with pytest.raises(ValidationError):
        AISMessage5(**invalid_message_5_data)
