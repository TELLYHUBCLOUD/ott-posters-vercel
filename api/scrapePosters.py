import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from lib.db import db
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
OTT_PLATFORMS = {
    'netflix': 'https://www.netflix.com/in/',
    'prime': 'https://www.primevideo.com/',
    'disney': 'https://www.hotstar.com/in',
    'hbo': 'https://www.hbomax.com/'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_platform(platform: str) -> List[Dict]:
    """Scrape posters from a specific OTT platform"""
    try:
        logger.info(f"Starting scrape for {platform}")
        response = requests.get(OTT_PLATFORMS[platform], headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        posters = []
        
        # Netflix scraping logic
        if platform == 'netflix':
            items = soup.select('.title-card-container')
            for item in items:
                try:
                    img_tag = item.select_one('img')
                    title_tag = item.select_one('.title-card-title')
                    
                    if img_tag and title_tag:
                        poster = {
                            'title': title_tag.text.strip(),
                            'image_url': img_tag['src'],
                            'platform': platform,
                            'source_url': OTT_PLATFORMS[platform],
                            'scraped_at': datetime.utcnow()
                        }
                        posters.append(poster)
                except Exception as e:
                    logger.warning(f"Error parsing item: {e}")
        
        # Add other platform scraping logic here...
        
        logger.info(f"Found {len(posters)} posters for {platform}")
        return posters
        
    except Exception as e:
        logger.error(f"Error scraping {platform}: {e}")
        return []

def update_json_file(posters: List[Dict]):
    """Maintain a JSON backup of posters"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'ott-posters.json')
        existing_data = []
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                existing_data = json.load(f)
        
        # Merge and deduplicate by image_url
        merged = {p['image_url']: p for p in existing_data}
        merged.update({p['image_url']: p for p in posters})
        
        with open(json_path, 'w') as f:
            json.dump(list(merged.values()), f, indent=2)
            
        logger.info(f"Updated JSON backup with {len(merged)} posters")
        
    except Exception as e:
        logger.error(f"Error updating JSON file: {e}")

def scrape_all_platforms() -> Dict[str, List[Dict]]:
    """Scrape all configured platforms"""
    results = {}
    for platform in OTT_PLATFORMS:
        posters = scrape_platform(platform)
        if posters:
            inserted_ids = db.save_to_db(posters)
            update_json_file(posters)
            results[platform] = {
                'count': len(inserted_ids),
                'sample': posters[0] if posters else None
            }
    return results

def handler(event, context):
    """Vercel serverless function handler"""
    try:
        platform = event.get('queryStringParameters', {}).get('platform')
        
        if platform and platform in OTT_PLATFORMS:
            posters = scrape_platform(platform)
            inserted_ids = db.save_to_db(posters)
            update_json_file(posters)
            message = f"Scraped {len(inserted_ids)} posters from {platform}"
        else:
            results = scrape_all_platforms()
            message = f"Scraped all platforms: {results}"
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
