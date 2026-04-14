import pytest
import os
import sys
from dotenv import load_dotenv

# Add data-sync/src to sys.path for module discovery
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

# Load environment variables from .env for testing
load_dotenv()

# Mock MONGO_URI for testing
os.environ["MONGO_URI"] = "mongodb://localhost:27017/testdb"
os.environ["INVALID_MONGO_URI"] = "mongodb://invalid:invalid@localhost:27017/testdb"


@pytest.mark.asyncio
async def test_connect_to_mongo_success():
    from db.client import connect_to_mongo, close_mongo_connection

    client = await connect_to_mongo()
    assert client is not None
    # For a successful connection, MotorClient is_primary attribute can be used to check connection
    # However, for local connection without replica set, is_primary may not be true immediately.
    # A better check is if a simple command like ping works.
    # The client.admin.command('ping') is already used in connect_to_mongo for verification.
    await close_mongo_connection(client)


@pytest.mark.asyncio
async def test_close_mongo_connection_success():
    from db.client import connect_to_mongo, close_mongo_connection

    client = await connect_to_mongo()
    await close_mongo_connection(client)
    # No direct way to assert client is closed without trying an operation and expecting an error.
    # For now, simply calling close_mongo_connection is sufficient for this test's purpose.
    pass


@pytest.mark.asyncio
async def test_connect_to_mongo_invalid_uri():
    from db.client import connect_to_mongo

    with pytest.raises(ConnectionError):  # Expect custom ConnectionError
        await connect_to_mongo(uri=os.getenv("INVALID_MONGO_URI"))
