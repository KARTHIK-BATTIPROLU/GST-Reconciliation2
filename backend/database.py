"""
Database connection managers for MongoDB Atlas and Neo4j Aura.

Both use singleton patterns — one connection per process, reused everywhere.
All credentials are loaded from environment variables.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from neo4j import GraphDatabase
import certifi

from backend.utils.logger import get_logger
from backend.config import get_settings

logger = get_logger(__name__)
settings = get_settings()

# ────────────────────────────────────────────
# Singleton holders
# ────────────────────────────────────────────
_mongo_client: AsyncIOMotorClient | None = None
_neo4j_driver = None


# ════════════════════════════════════════════
# MongoDB (async via Motor)
# ════════════════════════════════════════════

def get_mongo_client() -> AsyncIOMotorClient:
    """Return the singleton Motor client, creating it on first call."""
    global _mongo_client
    if _mongo_client is None:
        uri = settings.MONGO_URI
        _mongo_client = AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=60000,
            tlsCAFile=certifi.where(),
        )
    return _mongo_client


def get_mongo_db():
    """Return the default MongoDB database handle."""
    return get_mongo_client()[settings.MONGO_DB_NAME]



async def ping_mongo() -> bool:
    """Return True if MongoDB Atlas responds to a ping."""
    try:
        result = await get_mongo_client().admin.command("ping")
        return result.get("ok") == 1.0
    except Exception as exc:
        logger.error(f"MongoDB ping failed: {exc}")
        return False


# ════════════════════════════════════════════
# Neo4j Aura (sync driver — lightweight)
# ════════════════════════════════════════════

def get_neo4j_driver():
    """Return the singleton Neo4j driver, creating it on first call."""
    global _neo4j_driver
    if _neo4j_driver is None:
        uri = settings.NEO4J_URI
        user = settings.NEO4J_USER
        password = settings.NEO4J_PASSWORD
        
        _neo4j_driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=10,
            connection_acquisition_timeout=10,
        )
    return _neo4j_driver


def ping_neo4j() -> bool:
    """Return True if Neo4j Aura responds to a connectivity check."""
    try:
        driver = get_neo4j_driver()
        driver.verify_connectivity()
        return True
    except Exception as exc:
        logger.error(f"Neo4j ping failed: {exc}")
        return False



# ════════════════════════════════════════════
# Cleanup
# ════════════════════════════════════════════

async def close_connections():
    """Gracefully close both database connections."""
    global _mongo_client, _neo4j_driver

    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None

    if _neo4j_driver is not None:
        _neo4j_driver.close()
        _neo4j_driver = None
