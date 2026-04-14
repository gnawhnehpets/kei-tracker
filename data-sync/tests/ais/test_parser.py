import pytest
import json
from pydantic import ValidationError

from src.ais.parser import parse_ais_message
from src.models.ais import AISMessage3, AISMessage, MetaData

# Sample Message3 JSON from the plan context
SAMPLE_MESSAGE3_JSON = """
{
  "Message": {
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
      "COMM_STATE": {
        "SYNC_STATE": 0,
        "SLOT_TIMEOUT": 0,
        "RECEIVE_SLOTS": 0
      }
    }
  },
  "MetaData": {
    "time_utc": "2023-03-15T12:00:00Z",
    "mmsi": 123456789,
    "type": "AISMessage",
    "lon": -70.1234,
    "lat": 40.5678
  }
}
"""

# Placeholder for Message5 JSON (will need to be updated with actual sample if available)
SAMPLE_MESSAGE5_JSON = """
{
  "Message": {
    "Message5": {
      "MMSI": 987654321,
      "IMONumber": 1234567,
      "VesselName": "TEST VESSEL",
      "CallSign": "ABCD",
      "VesselType": 70,
      "Length": 100,
      "Breadth": 20,
      "FixDevice": 1,
      "ETA": "04-15 12:00",
      "Draught": 5.5,
      "Destination": "PORT A"
    }
  },
  "MetaData": {
    "time_utc": "2023-03-15T12:00:00Z",
    "mmsi": 987654321,
    "type": "AISMessage",
    "lon": -60.0,
    "lat": 30.0
  }
}
"""


def test_parse_ais_message_message3_success():
    parsed_message = parse_ais_message(SAMPLE_MESSAGE3_JSON)
    assert isinstance(parsed_message, AISMessage)
    assert isinstance(parsed_message.Message["Message3"], AISMessage3)
    assert parsed_message.MetaData.mmsi == 123456789


@pytest.mark.skip(
    reason="Message5 model placeholder, implement when actual Message5 JSON is available"
)
def test_parse_ais_message_message5_success():
    # This test will initially be skipped until a proper Message5 structure is confirmed
    parsed_message = parse_ais_message(SAMPLE_MESSAGE5_JSON)
    assert isinstance(parsed_message, AISMessage)
    # assert isinstance(parsed_message.Message["Message5"], AISMessage5) # Uncomment and fix when Message5 model is finalized
    assert parsed_message.MetaData.mmsi == 987654321


def test_parse_ais_message_unknown_type():
    unknown_json = """
    {
      "Message": {
        "UnknownMessage": {"id": 123}
      },
      "MetaData": {
        "time_utc": "2023-03-15T12:00:00Z",
        "mmsi": 123,
        "type": "AISMessage",
        "lon": 0.0,
        "lat": 0.0
      }
    }
    """
    parsed_message = parse_ais_message(unknown_json)
    assert (
        parsed_message is None
    )  # Or raises a specific error, depending on implementation choice


def test_parse_ais_message_invalid_json():
    invalid_json = "This is not valid JSON"
    with pytest.raises(json.JSONDecodeError):
        parse_ais_message(invalid_json)
