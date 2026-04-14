import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Load environment variables from .env
load_dotenv()


class ConnectionError(Exception):
    """Custom exception for MongoDB connection errors."""

    pass


async def connect_to_mongo(uri: str = None) -> AsyncIOMotorClient:
    """
    Establishes a connection to MongoDB.
    Args:
        uri: MongoDB connection URI. If None, it defaults to MONGO_URI from environment variables.
    Returns:
        An instance of AsyncIOMotorClient.
    Raises:
        ConnectionError: If connection fails.
    """
    if uri is None:
        uri = os.getenv("MONGO_URI")

    if not uri:
        raise ConnectionError("MONGO_URI environment variable not set or provided.")

    try:
        client = AsyncIOMotorClient(uri)
        # The is_primary property will attempt to connect and check the primary status
        # This will raise an exception if connection fails
        await client.admin.command("ping")
        print("MongoDB connection established.")
        return client
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")


async def close_mongo_connection(client: AsyncIOMotorClient):
    """
    Closes the MongoDB connection.
    Args:
        client: The AsyncIOMotorClient instance to close.
    """
    if client:
        client.close()
        print("MongoDB connection closed.")


# For direct execution and testing purposes (optional)
async def main():
    try:
        client = await connect_to_mongo()
        # Perform some operations here
        await close_mongo_connection(client)
    except ConnectionError as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
