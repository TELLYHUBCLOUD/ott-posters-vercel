from fastapi import FastAPI, Request
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main page with posters"""
    try:
        with open('ott-posters.json', 'r') as f:
            posters = json.load(f)
    except:
        posters = []
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posters": posters[:20]}
    )

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
