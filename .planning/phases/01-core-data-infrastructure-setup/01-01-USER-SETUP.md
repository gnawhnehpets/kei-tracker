# Phase 01: Core Data Infrastructure Setup - User Setup

## MongoDB Configuration

**Service:** MongoDB

**Why:** Persistent storage for ship data.

### Environment Variables

| Name       | Source                                                         |
|------------|----------------------------------------------------------------|
| `MONGO_URI` | Your MongoDB instance connection string (e.g., MongoDB Atlas, local Docker)|

### Dashboard Configuration

No specific dashboard configuration steps are required through this plan. Ensure your MongoDB instance is accessible via the provided `MONGO_URI`.

### Local Development Notes

To run MongoDB locally for development, you can use Docker:

```bash
docker run -d -p 27017:27017 --name mongo-dev mongo:latest
```

Then, set `MONGO_URI` to `mongodb://localhost:27017/your_database_name` (replace `your_database_name` with your desired database name).

### Verification Commands

To verify your MongoDB connection (assuming Python environment is set up):

```bash
# Navigate to your data-sync service directory
cd data-sync

# Ensure MONGO_URI is set in your environment or a .env file
export MONGO_URI="mongodb://localhost:27017/testdb" # Replace with your actual URI

# Run the connection test (assuming pytest is installed)
PYTHONPATH=src pytest tests/db/test_client.py
```

This should run the connection tests, which will attempt to connect to your MongoDB instance. If successful, all tests (except for the intentionally invalid URI test which should pass by raising ConnectionError) should pass.
