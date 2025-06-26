from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from lib.db import db  # MongoDB instance
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Platforms to scrape
PLATFORMS = {
    "netflix": {
        "url": "https://www.netflix.com/in/",
        "selectors": {
            "container": ".title-card-container",
            "title": ".title-card-title",
            "image": "img",
            "year": ".year"  # Example additional field
        }
    },
    "prime": {
        "url": "https://www.primevideo.com/",
        "selectors": {
            "container": ".tst-hover-container",
            "title": ".tst-title",
            "image": "img"
        }
    }
}

async def scrape_platform(platform: str):
    """Scrape posters from a specific platform"""
    try:
        config = PLATFORMS[platform]
        response = requests.get(config["url"], headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        posters = []
        
        for item in soup.select(config["selectors"]["container"]):
            try:
                posters.append({
                    "title": item.select_one(config["selectors"]["title"]).text.strip(),
                    "image_url": item.select_one(config["selectors"]["image"])["src"],
                    "platform": platform,
                    "scraped_at": datetime.utcnow(),
                    "metadata": {
                        "year": item.select_one(config["selectors"].get("year")).text.strip() 
                        if config["selectors"].get("year") else None
                    }
                })
            except Exception as e:
                logger.warning(f"Failed to parse item: {e}")
                continue
        
        # Save to MongoDB
        inserted_ids = db.save_to_db(posters)
        logger.info(f"Inserted {len(inserted_ids)} posters for {platform}")
        return posters
        
    except Exception as e:
        logger.error(f"Scrape failed for {platform}: {e}")
        raise HTTPException(500, f"Scrape failed: {str(e)}")

@router.get("/scrape/{platform}")
async def scrape_endpoint(platform: str):
    """API endpoint to trigger scraping"""
    if platform not in PLATFORMS:
        raise HTTPException(400, "Unsupported platform")
    
    posters = await scrape_platform(platform)
    return {
        "status": "success",
        "count": len(posters),
        "platform": platform,
        "sample": posters[0] if posters else None
    }

@router.get("/scrape-all")
async def scrape_all():
    """Scrape all supported platforms"""
    results = {}
    for platform in PLATFORMS:
        try:
            posters = await scrape_platform(platform)
            results[platform] = {
                "count": len(posters),
                "sample": posters[0] if posters else None
            }
        except Exception as e:
            results[platform] = {"error": str(e)}
    
    return {"results": results}
