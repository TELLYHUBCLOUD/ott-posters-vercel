from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('MONGODB_DBNAME', 'ott_posters')
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def save_to_db(self, posters):
        """Save posters to MongoDB"""
        try:
            collection = self.db.posters
            result = collection.insert_many(
                posters,
                ordered=False  # Continue on duplicate key errors
            )
            logger.info(f"Inserted {len(result.inserted_ids)} posters")
            return result.inserted_ids
        except Exception as e:
            logger.error(f"Error saving posters: {e}")
            return []

    def get_recent_posters(self, platform=None, limit=10):
        """Retrieve recent posters from MongoDB"""
        try:
            collection = self.db.posters
            query = {}
            if platform:
                query['platform'] = platform
            
            posters = collection.find(query).sort(
                'scraped_at', -1  # Descending order
            ).limit(limit)
            
            return list(posters)
        except Exception as e:
            logger.error(f"Error retrieving posters: {e}")
            return []

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

# Singleton instance
db = MongoDB()
