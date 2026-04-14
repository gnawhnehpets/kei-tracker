import pytest
import os
from dotenv import load_dotenv

# Load environment variables from .env for testing
load_dotenv()

# Mock MONGO_URI for testing
os.environ["MONGO_URI"] = "mongodb://localhost:27017/testdb"
os.environ["INVALID_MONGO_URI"] = "mongodb://invalid:invalid@localhost:27017/testdb"


@pytest.mark.asyncio
async def test_connect_to_mongo_success():
    from data_sync.src.db.client import connect_to_mongo, close_mongo_connection

    client = await connect_to_mongo()
    assert client is not None
    assert client.is_primary == True  # Motor client will verify connection
    await close_mongo_connection(client)


@pytest.mark.asyncio
async def test_close_mongo_connection_success():
    from data_sync.src.db.client import connect_to_mongo, close_mongo_connection

    client = await connect_to_mongo()
    await close_mongo_connection(client)
    # After closing, further operations should fail or client should be marked as closed
    # This assertion is a placeholder, as Motor client doesn't have a direct 'is_closed' attribute easily verifiable
    # A more robust test would involve trying an operation after close and expecting an error
    pass


@pytest.mark.asyncio
async def test_connect_to_mongo_invalid_uri():
    from data_sync.src.db.client import connect_to_mongo

    with pytest.raises(Exception):  # Expect a general exception for now, refine later
        await connect_to_mongo(uri=os.getenv("INVALID_MONGO_URI"))
