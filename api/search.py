from fastapi import APIRouter, HTTPException
from lib.db import db
from typing import Optional

router = APIRouter()

@router.get("/search")
async def search_posters(
    query: str,
    platform: Optional[str] = None,
    limit: int = 10,
    min_score: float = 1.0
):
    """
    Search posters by title with:
    - Full-text search
    - Platform filtering
    - Relevance scoring
    """
    try:
        results = db.search_posters(
            query=query,
            platform=platform,
            limit=limit,
            min_score=min_score
        )
        
        return {
            "status": "success",
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(500, f"Search failed: {str(e)}")
