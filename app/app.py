"""FastAPI application for Content Journey Finder."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from app.journey_planner import JourneyPlanner

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Content Journey Finder",
    description="A travel finder style application for discovering movies and TV shows",
    version="0.1.0"
)

# Setup static files and templates
app_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(app_dir / "static")), name="static")
templates = Jinja2Templates(directory=str(app_dir / "templates"))

# Initialize journey planner
planner = JourneyPlanner()


# Pydantic models for request validation
class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class JourneyRequest(BaseModel):
    duration: int = 180
    preferences: str = ""
    content_type: Optional[str] = None


class SuccessResponse(BaseModel):
    success: bool
    

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/search")
async def search(request: SearchRequest):
    """Search for content."""
    try:
        contents = planner.search_content(request.query, limit=request.limit)
        return {
            'success': True,
            'contents': [c.to_dict() for c in contents]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/semantic-search")
async def semantic_search(request: SearchRequest):
    """Perform semantic search."""
    try:
        contents = planner.semantic_search(request.query, limit=request.limit)
        return {
            'success': True,
            'contents': [c.to_dict() for c in contents]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/plan-journey")
async def plan_journey(request: JourneyRequest):
    """Plan a content viewing journey."""
    try:
        journey = planner.create_journey(
            target_duration=request.duration,
            preferences=request.preferences if request.preferences else None,
            content_type=request.content_type
        )
        return {
            'success': True,
            'journey': journey.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)
