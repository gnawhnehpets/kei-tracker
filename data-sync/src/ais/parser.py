import json
from typing import Optional, Any, Dict
from pydantic import ValidationError

from src.models.ais import AISMessage3, AISMessage5, AISMessage, MetaData


def parse_ais_message(raw_message_json: str) -> Optional[AISMessage]:
    try:
        data = json.loads(raw_message_json)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON input: {e}", e.doc, e.pos)

    # Validate top-level structure with AISMessage first
    try:
        ais_message_envelope = AISMessage(**data)
    except ValidationError:
        # If the top-level structure is not valid, return None or raise specific error
        return None

    # Determine message type and parse inner message
    message_content = ais_message_envelope.Message
    if "Message3" in message_content:
        try:
            message3_data = message_content["Message3"]
            # Pydantic's parse_obj will handle alias for LONGITUDE and LATITUDE
            parsed_message3 = AISMessage3.model_validate(message3_data)
            ais_message_envelope.Message = {"Message3": parsed_message3}
            return ais_message_envelope
        except ValidationError:
            return None  # Or raise a specific error
    elif "Message5" in message_content:
        try:
            message5_data = message_content["Message5"]
            parsed_message5 = AISMessage5.model_validate(message5_data)
            ais_message_envelope.Message = {"Message5": parsed_message5}
            return ais_message_envelope
        except ValidationError:
            return None  # Or raise a specific error
    # Add more message types as needed

    return None  # Unknown message type
