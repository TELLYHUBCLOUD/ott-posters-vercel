from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

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
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'ott-posters.json')
        with open(json_path, 'r') as f:
            all_posters = json.load(f)
        
        filtered = [p for p in all_posters if p['platform'] == platform][:limit]
        return {"status": "success", "data": filtered}
    except Exception as e:
        return {"status": "error", "message": str(e)}
