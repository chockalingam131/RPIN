"""
Standalone FastAPI app for Vercel deployment
Minimal version that works without complex imports
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI(
    title="RPIN - Rural Producer Intelligence Network",
    version="1.0.0",
    description="AI-powered market recommendation system for rural producers"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PredictionRequest(BaseModel):
    village_location: str
    crop_type: str
    quantity_kg: float
    harvest_date: date

class MarketRecommendation(BaseModel):
    market_id: str
    market_name: str
    predicted_price: float
    demand_level: str
    spoilage_risk_percent: float
    distance_km: float
    transport_cost: float
    net_profit: float

class PredictionResponse(BaseModel):
    request_id: str
    village_location: str
    crop_type: str
    quantity_kg: float
    markets: List[MarketRecommendation]
    best_market: str
    explanation: str

# Sample data
CROPS = {
    "tomato": {"name": "Tomato", "base_price": 25},
    "onion": {"name": "Onion", "base_price": 20},
    "potato": {"name": "Potato", "base_price": 15},
    "cabbage": {"name": "Cabbage", "base_price": 18},
    "carrot": {"name": "Carrot", "base_price": 22},
    "cauliflower": {"name": "Cauliflower", "base_price": 28}
}

MARKETS = {
    "madurai": {"name": "Madurai Mandi", "location": "Madurai"},
    "chennai": {"name": "Chennai Koyambedu", "location": "Chennai"},
    "coimbatore": {"name": "Coimbatore Market", "location": "Coimbatore"},
    "trichy": {"name": "Trichy Market", "location": "Trichy"},
    "salem": {"name": "Salem Market", "location": "Salem"},
    "erode": {"name": "Erode Market", "location": "Erode"}
}

DISTANCES = {
    "theni": {"madurai": 80, "chennai": 450, "coimbatore": 180, "trichy": 120, "salem": 200, "erode": 160},
    "dindigul": {"madurai": 65, "chennai": 420, "coimbatore": 160, "trichy": 90, "salem": 180, "erode": 140},
    "salem": {"madurai": 200, "chennai": 340, "coimbatore": 120, "trichy": 180, "salem": 0, "erode": 60},
    "erode": {"madurai": 160, "chennai": 400, "coimbatore": 90, "trichy": 140, "salem": 60, "erode": 0},
    "namakkal": {"madurai": 180, "chennai": 360, "coimbatore": 100, "trichy": 160, "salem": 40, "erode": 50},
    "karur": {"madurai": 120, "chennai": 380, "coimbatore": 140, "trichy": 80, "salem": 120, "erode": 100},
    "tirupur": {"madurai": 140, "chennai": 420, "coimbatore": 50, "trichy": 120, "salem": 80, "erode": 40},
    "pollachi": {"madurai": 160, "chennai": 480, "coimbatore": 40, "trichy": 140, "salem": 120, "erode": 80}
}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve simple frontend"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RPIN - Rural Producer Intelligence Network</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 800px; margin: 0 auto; }
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 20px;
            }
            h1 { color: #667eea; margin-bottom: 10px; }
            .status { color: #28a745; font-weight: bold; font-size: 1.2em; margin: 20px 0; }
            a { color: #667eea; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            ul { margin: 20px 0; padding-left: 20px; }
            li { margin: 10px 0; }
            pre {
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>🌾 RPIN - Rural Producer Intelligence Network</h1>
                <p class="status">✅ API is running successfully!</p>
                <p>AI-powered market recommendation system for rural producers.</p>
                
                <h2 style="margin-top: 30px;">📚 Available Endpoints:</h2>
                <ul>
                    <li><a href="/docs">📖 Interactive API Documentation (Swagger UI)</a></li>
                    <li><a href="/health">💚 Health Check</a></li>
                    <li><a href="/api/v1/crops">🌱 List Available Crops</a></li>
                    <li><a href="/api/v1/markets">🏪 List Available Markets</a></li>
                </ul>
                
                <h2 style="margin-top: 30px;">🧪 Quick Test:</h2>
                <p>Use the <a href="/docs">Interactive API Documentation</a> to test predictions.</p>
                
                <p style="margin-top: 20px;"><strong>Sample Request:</strong></p>
                <pre>POST /api/v1/predict
{
  "village_location": "theni",
  "crop_type": "tomato",
  "quantity_kg": 1000,
  "harvest_date": "2024-03-15"
}</pre>
                
                <p style="margin-top: 20px;"><strong>Supported Villages:</strong> theni, dindigul, salem, erode, namakkal, karur, tirupur, pollachi</p>
                <p><strong>Supported Crops:</strong> tomato, onion, potato, cabbage, carrot, cauliflower</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "RPIN - Rural Producer Intelligence Network",
        "version": "1.0.0"
    }

@app.get("/api/v1/crops")
async def list_crops():
    """List available crops"""
    return {"crops": [{"id": k, **v} for k, v in CROPS.items()]}

@app.get("/api/v1/markets")
async def list_markets():
    """List available markets"""
    return {"markets": [{"id": k, **v} for k, v in MARKETS.items()]}

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make market prediction"""
    import random
    from datetime import datetime
    
    # Validate inputs
    if request.village_location.lower() not in DISTANCES:
        return {"error": f"Village '{request.village_location}' not supported"}
    
    if request.crop_type.lower() not in CROPS:
        return {"error": f"Crop '{request.crop_type}' not supported"}
    
    # Get data
    village_distances = DISTANCES[request.village_location.lower()]
    crop_data = CROPS[request.crop_type.lower()]
    base_price = crop_data["base_price"]
    
    # Generate recommendations
    recommendations = []
    for market_id, distance in village_distances.items():
        market_data = MARKETS[market_id]
        
        # Simple price prediction (base + random variation)
        predicted_price = base_price + random.uniform(-3, 8)
        
        # Demand level based on price
        if predicted_price > base_price + 3:
            demand_level = "High"
        elif predicted_price < base_price - 2:
            demand_level = "Low"
        else:
            demand_level = "Medium"
        
        # Spoilage risk based on distance
        spoilage_risk = min(100, (distance / 10) + random.uniform(0, 5))
        
        # Transport cost (₹4 per km per quintal)
        quintals = request.quantity_kg / 100
        transport_cost = distance * 4 * quintals
        
        # Net profit
        revenue = predicted_price * request.quantity_kg
        net_profit = revenue - transport_cost
        
        recommendations.append(MarketRecommendation(
            market_id=market_id,
            market_name=market_data["name"],
            predicted_price=round(predicted_price, 2),
            demand_level=demand_level,
            spoilage_risk_percent=round(spoilage_risk, 1),
            distance_km=distance,
            transport_cost=round(transport_cost, 2),
            net_profit=round(net_profit, 2)
        ))
    
    # Sort by net profit
    recommendations.sort(key=lambda x: x.net_profit, reverse=True)
    
    # Generate explanation
    best = recommendations[0]
    explanation = (
        f"For {request.quantity_kg}kg of {crop_data['name']} from {request.village_location.title()}, "
        f"selling in {best.market_name} gives ₹{best.net_profit:,.0f} profit. "
        f"This market offers the best price (₹{best.predicted_price:.2f}/kg) with {best.demand_level.lower()} demand "
        f"and manageable transport cost (₹{best.transport_cost:,.0f} for {best.distance_km}km)."
    )
    
    return PredictionResponse(
        request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        village_location=request.village_location,
        crop_type=request.crop_type,
        quantity_kg=request.quantity_kg,
        markets=recommendations,
        best_market=best.market_name,
        explanation=explanation
    )
