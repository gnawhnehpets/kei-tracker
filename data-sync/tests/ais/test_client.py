import pytest
import asyncio
from unittest.mock import AsyncMock

import json

# This will fail because client.py does not exist yet
from src.ais.client import connect_to_aisstream, receive_ais_message


@pytest.fixture
def mock_websocket(mocker):
    mock_connect = mocker.patch("websockets.connect", new_callable=mocker.AsyncMock)
    mock_connect.return_value.__aenter__.return_value = (
        AsyncMock()
    )  # This is the actual websocket object
    yield mock_connect


@pytest.mark.asyncio
async def test_connect_to_aisstream_success(mock_websocket, mocker):
    mocker.patch("os.getenv", return_value="test_api_key")
    client = await connect_to_aisstream()
    assert client is not None
    mock_websocket.assert_called_once_with(
        "wss://stream.aisstream.io/v0/stream?apiKey=test_api_key"
    )


@pytest.mark.asyncio
async def test_receive_ais_message_success(mock_websocket, mocker):
    mocker.patch("os.getenv", return_value="test_api_key")
    client = await connect_to_aisstream()
    client.recv.return_value = json.dumps({"test": "message"})
    message = await receive_ais_message(client)
    assert message == {"test": "message"}
    client.recv.assert_called_once()


@pytest.mark.asyncio
async def test_connect_to_aisstream_failure(mock_websocket, mocker):
    mock_websocket.side_effect = ConnectionRefusedError
    mocker.patch("os.getenv", return_value="test_api_key")
    with pytest.raises(ConnectionError):
        await connect_to_aisstream(url="wss://invalid.url")
