import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import json

# This will fail because client.py does not exist yet
from data_sync.src.ais.client import connect_to_aisstream, receive_ais_message


@pytest.fixture
def mock_websocket():
    with patch("websockets.connect") as mock_connect:
        mock_ws = AsyncMock()
        mock_connect.return_value.__aenter__.return_value = mock_ws
        yield mock_ws


@pytest.mark.asyncio
async def test_connect_to_aisstream_success(mock_websocket):
    with patch("os.getenv", return_value="test_api_key"):
        client = await connect_to_aisstream()
        assert client is not None
        mock_websocket.assert_called_once_with(
            "wss://stream.aisstream.io/v0/stream?apiKey=test_api_key"
        )


@pytest.mark.asyncio
async def test_receive_ais_message_success(mock_websocket):
    mock_websocket.recv.return_value = json.dumps({"test": "message"})
    message = await receive_ais_message(mock_websocket)
    assert message == {"test": "message"}
    mock_websocket.recv.assert_called_once()


@pytest.mark.asyncio
async def test_connect_to_aisstream_failure():
    with patch("websockets.connect", side_effect=ConnectionRefusedError):
        with patch("os.getenv", return_value="test_api_key"):
            with pytest.raises(ConnectionError):
                await connect_to_aisstream(url="wss://invalid.url")
