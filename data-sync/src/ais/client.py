import os
import json
import websockets


async def connect_to_aisstream(url: str = "wss://stream.aisstream.io/v0/stream"):
    api_key = os.getenv("AISSTREAM_API_KEY")
    if not api_key:
        raise ConnectionError("AISSTREAM_API_KEY environment variable not set.")

    full_url = f"{url}?apiKey={api_key}"
    try:
        # Ensure the connection is managed as an async context manager
        connection = await websockets.connect(full_url)
        return connection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to AISStream.io: {e}")


async def receive_ais_message(websocket) -> dict:
    try:
        message = await websocket.recv()
        return json.loads(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally.")
        return {}
    except Exception as e:
        raise IOError(f"Error receiving or decoding message: {e}")
