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
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPIN - Rural Producer Intelligence Network</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus { outline: none; border-color: #667eea; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .loading { text-align: center; padding: 40px; display: none; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .results { display: none; }
        .best-market {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        .best-market h2 { margin-bottom: 15px; }
        .profit { font-size: 2.5em; font-weight: bold; margin: 10px 0; }
        .explanation {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #667eea;
        }
        .markets-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .markets-table th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        .markets-table td { padding: 15px; border-bottom: 1px solid #e0e0e0; }
        .markets-table tr:hover { background: #f8f9fa; }
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-high { background: #d4edda; color: #155724; }
        .badge-medium { background: #fff3cd; color: #856404; }
        .badge-low { background: #f8d7da; color: #721c24; }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        .back-btn { background: #6c757d; margin-top: 20px; }
        @media (max-width: 768px) {
            .header h1 { font-size: 1.8em; }
            .card { padding: 20px; }
            .markets-table { font-size: 0.9em; }
            .markets-table th, .markets-table td { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌾 RPIN</h1>
            <p>Rural Producer Intelligence Network</p>
            <p style="font-size: 0.9em; margin-top: 5px;">AI-Powered Market Recommendations</p>
        </div>

        <div class="card" id="inputForm">
            <h2 style="margin-bottom: 25px; color: #333;">Enter Your Details</h2>
            <div class="error" id="errorMessage"></div>
            <form id="predictionForm">
                <div class="form-group">
                    <label for="village">Village/Location</label>
                    <select id="village" required>
                        <option value="">Select your village</option>
                        <option value="theni">Theni</option>
                        <option value="dindigul">Dindigul</option>
                        <option value="salem">Salem</option>
                        <option value="erode">Erode</option>
                        <option value="namakkal">Namakkal</option>
                        <option value="karur">Karur</option>
                        <option value="tirupur">Tirupur</option>
                        <option value="pollachi">Pollachi</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="crop">Crop Type</label>
                    <select id="crop" required>
                        <option value="">Select your crop</option>
                        <option value="tomato">Tomato</option>
                        <option value="onion">Onion</option>
                        <option value="potato">Potato</option>
                        <option value="cabbage">Cabbage</option>
                        <option value="carrot">Carrot</option>
                        <option value="cauliflower">Cauliflower</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="quantity">Quantity (kg)</label>
                    <input type="number" id="quantity" min="1" max="100000" required placeholder="Enter quantity in kg">
                </div>
                <div class="form-group">
                    <label for="harvestDate">Harvest Date</label>
                    <input type="date" id="harvestDate" required>
                </div>
                <button type="submit" class="btn">Get Recommendations</button>
            </form>
        </div>

        <div class="card loading" id="loadingState">
            <div class="spinner"></div>
            <p style="color: #666; font-size: 1.1em;">Analyzing markets and calculating profits...</p>
        </div>

        <div class="results" id="resultsSection">
            <div class="card">
                <div class="best-market">
                    <h2>🎯 Recommended Market</h2>
                    <h3 id="bestMarketName"></h3>
                    <div class="profit" id="bestProfit"></div>
                    <p id="bestDetails"></p>
                </div>
                <div class="explanation">
                    <h3 style="margin-bottom: 15px; color: #333;">📊 Explanation</h3>
                    <p id="explanationText" style="line-height: 1.6; color: #555;"></p>
                </div>
                <h3 style="margin-bottom: 15px; color: #333;">All Market Options</h3>
                <div style="overflow-x: auto;">
                    <table class="markets-table">
                        <thead>
                            <tr>
                                <th>Market</th>
                                <th>Price (₹/kg)</th>
                                <th>Demand</th>
                                <th>Spoilage Risk</th>
                                <th>Distance (km)</th>
                                <th>Net Profit (₹)</th>
                            </tr>
                        </thead>
                        <tbody id="marketsTableBody"></tbody>
                    </table>
                </div>
                <button class="btn back-btn" onclick="resetForm()">New Prediction</button>
            </div>
        </div>
    </div>

    <script>
        const API_BASE_URL = '/api/v1';
        document.getElementById('harvestDate').min = new Date().toISOString().split('T')[0];
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        document.getElementById('harvestDate').max = maxDate.toISOString().split('T')[0];

        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            document.getElementById('errorMessage').style.display = 'none';
            
            const formData = {
                village_location: document.getElementById('village').value,
                crop_type: document.getElementById('crop').value,
                quantity_kg: parseFloat(document.getElementById('quantity').value),
                harvest_date: document.getElementById('harvestDate').value
            };

            document.getElementById('inputForm').style.display = 'none';
            document.getElementById('loadingState').style.display = 'block';

            try {
                const response = await fetch(`${API_BASE_URL}/predict`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get recommendations');
                }

                const data = await response.json();
                displayResults(data);
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('loadingState').style.display = 'none';
                document.getElementById('inputForm').style.display = 'block';
                const errorMsg = document.getElementById('errorMessage');
                errorMsg.textContent = error.message || 'Failed to get recommendations. Please try again.';
                errorMsg.style.display = 'block';
            }
        });

        function displayResults(data) {
            document.getElementById('loadingState').style.display = 'none';
            document.getElementById('resultsSection').style.display = 'block';

            const bestMarket = data.markets[0];
            document.getElementById('bestMarketName').textContent = bestMarket.market_name;
            document.getElementById('bestProfit').textContent = `₹${bestMarket.net_profit.toLocaleString('en-IN')}`;
            document.getElementById('bestDetails').textContent = 
                `Price: ₹${bestMarket.predicted_price.toFixed(2)}/kg | ` +
                `Demand: ${bestMarket.demand_level} | ` +
                `Distance: ${bestMarket.distance_km}km`;

            document.getElementById('explanationText').textContent = data.explanation;

            const tbody = document.getElementById('marketsTableBody');
            tbody.innerHTML = '';

            data.markets.forEach((market, index) => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td><strong>${market.market_name}</strong>${index === 0 ? ' ⭐' : ''}</td>
                    <td>₹${market.predicted_price.toFixed(2)}</td>
                    <td><span class="badge badge-${market.demand_level.toLowerCase()}">${market.demand_level}</span></td>
                    <td>${market.spoilage_risk_percent.toFixed(1)}%</td>
                    <td>${market.distance_km}km</td>
                    <td><strong>₹${market.net_profit.toLocaleString('en-IN')}</strong></td>
                `;
            });

            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }

        function resetForm() {
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('inputForm').style.display = 'block';
            document.getElementById('predictionForm').reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>"""
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
