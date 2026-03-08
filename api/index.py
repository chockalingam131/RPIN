from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import random

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
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
                    }
                    h1 { color: #667eea; margin-bottom: 10px; }
                    .status { color: #28a745; font-weight: bold; font-size: 1.2em; margin: 20px 0; }
                    a { color: #667eea; text-decoration: none; font-weight: bold; }
                    ul { margin: 20px 0; padding-left: 20px; }
                    li { margin: 10px 0; }
                    pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
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
                            <li><a href="/health">💚 Health Check</a></li>
                            <li><a href="/api/v1/crops">🌱 List Available Crops</a></li>
                            <li><a href="/api/v1/markets">🏪 List Available Markets</a></li>
                        </ul>
                        
                        <h2 style="margin-top: 30px;">🧪 Test Prediction:</h2>
                        <p>Send POST request to <code>/api/v1/predict</code></p>
                        <pre>{
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
            self.wfile.write(html.encode())
            
        elif path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "RPIN - Rural Producer Intelligence Network",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/v1/crops':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            crops_list = [{"id": k, **v} for k, v in CROPS.items()]
            self.wfile.write(json.dumps({"crops": crops_list}).encode())
            
        elif path == '/api/v1/markets':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            markets_list = [{"id": k, **v} for k, v in MARKETS.items()]
            self.wfile.write(json.dumps({"markets": markets_list}).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        if self.path == '/api/v1/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode())
                
                village = request_data.get('village_location', '').lower()
                crop = request_data.get('crop_type', '').lower()
                quantity = float(request_data.get('quantity_kg', 0))
                
                if village not in DISTANCES:
                    raise ValueError(f"Village '{village}' not supported")
                if crop not in CROPS:
                    raise ValueError(f"Crop '{crop}' not supported")
                
                village_distances = DISTANCES[village]
                crop_data = CROPS[crop]
                base_price = crop_data["base_price"]
                
                recommendations = []
                for market_id, distance in village_distances.items():
                    market_data = MARKETS[market_id]
                    
                    predicted_price = base_price + random.uniform(-3, 8)
                    
                    if predicted_price > base_price + 3:
                        demand_level = "High"
                    elif predicted_price < base_price - 2:
                        demand_level = "Low"
                    else:
                        demand_level = "Medium"
                    
                    spoilage_risk = min(100, (distance / 10) + random.uniform(0, 5))
                    quintals = quantity / 100
                    transport_cost = distance * 4 * quintals
                    revenue = predicted_price * quantity
                    net_profit = revenue - transport_cost
                    
                    recommendations.append({
                        "market_id": market_id,
                        "market_name": market_data["name"],
                        "predicted_price": round(predicted_price, 2),
                        "demand_level": demand_level,
                        "spoilage_risk_percent": round(spoilage_risk, 1),
                        "distance_km": distance,
                        "transport_cost": round(transport_cost, 2),
                        "net_profit": round(net_profit, 2)
                    })
                
                recommendations.sort(key=lambda x: x["net_profit"], reverse=True)
                best = recommendations[0]
                
                explanation = (
                    f"For {quantity}kg of {crop_data['name']} from {village.title()}, "
                    f"selling in {best['market_name']} gives ₹{best['net_profit']:,.0f} profit. "
                    f"This market offers the best price (₹{best['predicted_price']:.2f}/kg) with {best['demand_level'].lower()} demand."
                )
                
                response = {
                    "request_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "village_location": village,
                    "crop_type": crop,
                    "quantity_kg": quantity,
                    "markets": recommendations,
                    "best_market": best["market_name"],
                    "explanation": explanation
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
