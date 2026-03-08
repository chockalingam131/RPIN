"""
RPIN - Rural Producer Intelligence Network
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging

from app.core.config import settings
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered market recommendation system for rural producers"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve frontend"""
    try:
        from pathlib import Path
        public_dir = Path(__file__).parent.parent / "public"
        index_file = public_dir / "index.html"
        
        if index_file.exists():
            return index_file.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error loading frontend: {e}")
    
    # Fallback: Return simple HTML
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RPIN - Rural Producer Intelligence Network</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: white;
                color: #333;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; }
            a {
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }
            .status { color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 RPIN - Rural Producer Intelligence Network</h1>
            <p class="status">✅ API is running!</p>
            <p>AI-powered market recommendation system for rural producers.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><a href="/docs">📖 API Documentation (Swagger UI)</a></li>
                <li><a href="/health">💚 Health Check</a></li>
                <li><a href="/api/v1/crops">🌱 List Crops</a></li>
                <li><a href="/api/v1/markets">🏪 List Markets</a></li>
            </ul>
            <h2>Quick Test:</h2>
            <p>Use the <a href="/docs">API Documentation</a> to test the prediction endpoint.</p>
            <p><strong>Sample Request:</strong></p>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto;">
POST /api/v1/predict
{
  "village_location": "theni",
  "crop_type": "tomato",
  "quantity_kg": 1000,
  "harvest_date": "2024-03-15"
}</pre>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
