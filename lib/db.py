from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from typing import List, Dict, Optional

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
        self.ensure_indexes()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(
                self.uri,
                connectTimeoutMS=30000,
                socketTimeoutMS=None,
                socketKeepAlive=True,
                maxPoolSize=100
            )
            self.db = self.client[self.db_name]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def ensure_indexes(self):
        """Create necessary indexes on first run"""
        try:
            collection = self.db.posters
            
            # Platform index for filtering
            collection.create_index([('platform', ASCENDING)])
            
            # Scraped_at index for sorting
            collection.create_index([('scraped_at', DESCENDING)])
            
            # Text index for search
            collection.create_index([('title', TEXT)])
            
            # Compound index for platform + date queries
            collection.create_index([
                ('platform', ASCENDING),
                ('scraped_at', DESCENDING)
            ])
            
            # Unique index on image_url to prevent duplicates
            collection.create_index([('image_url', ASCENDING)], unique=True)
            
            logger.info("Database indexes created/verified")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

    def save_to_db(self, posters: List[Dict]) -> List[str]:
        """
        Save posters to MongoDB with bulk insert
        Args:
            posters: List of poster dictionaries
        Returns:
            List of inserted IDs (empty list if none inserted)
        """
        try:
            if not posters:
                return []
                
            collection = self.db.posters
            
            # Prepare documents with current timestamp if not provided
            for poster in posters:
                if 'scraped_at' not in poster:
                    poster['scraped_at'] = datetime.utcnow()
            
            # Bulk insert with ordered=False to continue on errors
            result = collection.insert_many(
                posters,
                ordered=False,
                bypass_document_validation=False
            )
            
            logger.info(f"Inserted {len(result.inserted_ids)} posters")
            return result.inserted_ids
            
        except Exception as e:
            logger.error(f"Error saving posters: {e}")
            return []

    def get_recent_posters(
        self, 
        platform: Optional[str] = None, 
        limit: int = 10
    ) -> List[Dict]:
        """
        Retrieve recent posters with optional platform filter
        Args:
            platform: Optional platform filter
            limit: Maximum number of results
        Returns:
            List of poster documents
        """
        try:
            collection = self.db.posters
            query = {'platform': platform} if platform else {}
            
            posters = list(collection.find(query)
                .sort('scraped_at', DESCENDING)
                .limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for poster in posters:
                poster['_id'] = str(poster['_id'])
                
            return posters
            
        except Exception as e:
            logger.error(f"Error retrieving posters: {e}")
            return []

    def get_posters_paginated(
        self,
        platform: Optional[str] = None,
        page: int = 1,
        per_page: int = 10
    ) -> Dict:
        """
        Get paginated results with total count
        Args:
            platform: Optional platform filter
            page: Page number (1-based)
            per_page: Items per page
        Returns:
            Dictionary with posters and pagination info
        """
        try:
            collection = self.db.posters
            query = {'platform': platform} if platform else {}
            
            total = collection.count_documents(query)
            skip = (page - 1) * per_page
            
            posters = list(collection.find(query)
                .sort('scraped_at', DESCENDING)
                .skip(skip)
                .limit(per_page))
                
            # Convert ObjectId to string
            for poster in posters:
                poster['_id'] = str(poster['_id'])
                
            return {
                'posters': posters,
                'pagination': {
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'total_pages': (total + per_page - 1) // per_page
                }
            }
            
        except Exception as e:
            logger.error(f"Error in paginated query: {e}")
            return {'posters': [], 'pagination': {}}

    def search_posters(self, query_text: str, limit: int = 10) -> List[Dict]:
        """
        Full-text search on poster titles
        Args:
            query_text: Search string
            limit: Maximum results
        Returns:
            List of matching posters
        """
        try:
            collection = self.db.posters
            
            results = list(collection.find(
                {'$text': {'$search': query_text}},
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})])
            .limit(limit))
            
            for poster in results:
                poster['_id'] = str(poster['_id'])
                
            return results
            
        except Exception as e:
            logger.error(f"Error in text search: {e}")
            return []

    def close(self):
        """Clean up MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Singleton instance
db = MongoDB()
