from fastapi import FastAPI
from api.scrape import router as scrape_router
from api.search import router as search_router

app = FastAPI()

# Include routers
app.include_router(scrape_router, prefix="/api")
app.include_router(search_router, prefix="/api")

# Health check
@app.get("/")
async def health_check():
    return {"status": "running"}
