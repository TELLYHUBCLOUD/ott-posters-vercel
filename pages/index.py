from fastapi import FastAPI, Request,  HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

# Templates
templates = Jinja2Templates(directory="public/templates")

@app.get("/")
async def read_root():
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'ott-posters.json')
        with open(json_path, 'r') as f:
            posters = json.load(f)
        return {"posters": posters[:20]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/posters")
async def get_posters(platform: str = "netflix", limit: int = 10):
    """API endpoint to get posters"""
    try:
        with open('ott-posters.json', 'r') as f:
            all_posters = json.load(f)
        
        filtered = [p for p in all_posters if p['platform'] == platform][:limit]
        return {"status": "success", "data": filtered}
    except Exception as e:
        return {"status": "error", "message": str(e)}
