import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from lib.db import db
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


# ... (other imports remain the same)

def scrape_ott_posters(platform):
    """Scrape posters from a specific OTT platform"""
    try:
        response = requests.get(OTT_PLATFORMS[platform], headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        posters = []
        
        # Example: Netflix poster scraping
        if platform == 'netflix':
            items = soup.select('.title-card-container')
            for item in items:
                poster = {
                    'title': item.select_one('.title-card-title').text.strip(),
                    'image_url': item.select_one('img')['src'],
                    'platform': platform,
                    'scraped_at': datetime.now()
                }
                posters.append(poster)
        
        # Save to MongoDB
        db.save_to_db(posters)
        update_json_file(posters)
        
        return posters
    
    except Exception as e:
        logger.error(f"Error scraping {platform}: {e}")
        return []
def update_json_file(data):
    """Update the JSON file with new posters"""
    try:
        existing_data = []
        if os.path.exists('ott-posters.json'):
            with open('ott-posters.json', 'r') as f:
                existing_data = json.load(f)
        
        # Merge and deduplicate
        merged_data = existing_data + data
        unique_data = {item['image_url']: item for item in merged_data}.values()
        
        with open('ott-posters.json', 'w') as f:
            json.dump(list(unique_data), f, indent=2)
            
    except Exception as e:
        print(f"Error updating JSON file: {e}")

def handler(event, context):
    """Vercel serverless function handler"""
    platform = event.query.get('platform', 'netflix')
    posters = scrape_ott_posters(platform)
    
    return {
        'statusCode': 200,
        'body': json.dumps(posters),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
