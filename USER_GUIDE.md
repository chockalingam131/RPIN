# RPIN User Guide

Complete guide for using the Rural Producer Intelligence Network application.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Running Locally](#running-locally)
3. [Using the Application](#using-the-application)
4. [Understanding Results](#understanding-results)
5. [API Usage](#api-usage)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### For Local Development

```bash
# 1. Start Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python main.py

# 2. Start Frontend (in new terminal)
cd frontend
python -m http.server 3000

# 3. Open Browser
# Visit: http://localhost:3000
```

### For AWS Deployment

```bash
# Backend URL: Your Elastic Beanstalk URL
# Frontend URL: Your S3/CloudFront URL
# See AWS_DEPLOYMENT_GUIDE.md for deployment steps
```

---

## 💻 Running Locally

### Step 1: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Start server
python main.py
```

**Expected Output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Backend is now running at**: http://localhost:8000

**API Documentation**: http://localhost:8000/docs

### Step 2: Start the Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Start simple HTTP server
python -m http.server 3000
```

**Frontend is now running at**: http://localhost:3000

### Step 3: Access the Application

Open your browser and visit: **http://localhost:3000**

---

## 📱 Using the Application

### Main Interface

The application has a simple, user-friendly interface with the following sections:

1. **Header**: Shows the RPIN logo and tagline
2. **Input Form**: Where you enter your details
3. **Results Section**: Shows recommendations after submission

### Step-by-Step Usage

#### 1. Enter Your Details

**Village/Location**
- Select your village from the dropdown
- Available villages: Theni, Dindigul, Salem, Erode, Namakkal, Karur, Tirupur, Pollachi

**Crop Type**
- Select the crop you want to sell
- Available crops: Tomato, Onion, Potato, Cabbage, Carrot, Cauliflower

**Quantity (kg)**
- Enter the quantity in kilograms
- Minimum: 1 kg
- Maximum: 100,000 kg
- Example: 1000 for 1 ton

**Harvest Date**
- Select when you plan to harvest
- Must be today or in the future
- Maximum: 30 days from today
- Use the date picker for easy selection

#### 2. Submit the Form

Click the **"Get Recommendations"** button

The system will:
- Validate your input
- Analyze multiple markets
- Calculate profits for each market
- Predict prices for the next 7 days
- Assess spoilage risks
- Calculate transport costs
- Generate recommendations

**Processing Time**: 2-5 seconds

#### 3. View Results

The results page shows:

**Best Market Recommendation** (Green Box)
- Market name
- Expected profit in ₹
- Price per kg
- Demand level
- Distance

**Explanation** (Gray Box)
- Natural language explanation
- Key factors affecting the recommendation
- Comparison with other markets
- Important notes about spoilage or distance

**All Market Options** (Table)
- Complete comparison of all nearby markets
- Sorted by profit (highest first)
- Shows:
  - Market name (⭐ for best)
  - Price per kg
  - Demand level (High/Medium/Low)
  - Spoilage risk percentage
  - Distance in km
  - Net profit in ₹

#### 4. Make a New Prediction

Click **"New Prediction"** button to return to the input form

---

## 📊 Understanding Results

### Best Market Recommendation

**Example**:
```
🎯 Recommended Market
Madurai Mandi
₹20,800
Price: ₹28.50/kg | Demand: High | Distance: 80km
```

**What this means**:
- **Market**: Madurai Mandi is the best option
- **Profit**: You'll make ₹20,800 net profit
- **Price**: Market price is ₹28.50 per kg
- **Demand**: High demand means good selling conditions
- **Distance**: 80 km from your village

### Explanation

**Example**:
```
For 1,000 kg of tomatoes from Theni, selling in Madurai Mandi 
after 3 days gives ₹20,800 profit which is ₹7,300 more than 
Coimbatore Market due to rising prices, lower spoilage risk, 
and shorter distance.
```

**Key Information**:
- **Quantity**: Your input quantity
- **Crop**: Your selected crop
- **Village**: Your location
- **Best Market**: Recommended market
- **Timing**: When to sell
- **Profit**: Expected profit
- **Comparison**: How much better than alternatives
- **Reasons**: Why this market is best

### Market Comparison Table

**Columns Explained**:

1. **Market**: Market name (⭐ indicates best option)
2. **Price (₹/kg)**: Predicted selling price per kilogram
3. **Demand**: Market demand level
   - 🟢 **High**: Strong demand, good selling conditions
   - 🟡 **Medium**: Moderate demand, average conditions
   - 🔴 **Low**: Weak demand, may be harder to sell
4. **Spoilage Risk**: Percentage of crop that may spoil
   - <10%: Low risk ✅
   - 10-20%: Medium risk ⚠️
   - >20%: High risk ❌
5. **Distance (km)**: Distance from your village
6. **Net Profit (₹)**: Expected profit after all costs

### Demand Levels

**High Demand** 🟢
- Prices are rising
- Good time to sell
- Market has strong buying interest
- Lower risk of unsold inventory

**Medium Demand** 🟡
- Stable prices
- Normal market conditions
- Average selling conditions

**Low Demand** 🔴
- Prices are falling
- Market may be oversupplied
- May take longer to sell
- Consider waiting or choosing different market

### Spoilage Risk

**Factors Affecting Spoilage**:
- Crop type and shelf life
- Transport duration
- Weather conditions (temperature, humidity)
- Distance to market
- Handling requirements

**Risk Categories**:
- **Low (<10%)**: Safe to transport, minimal losses
- **Medium (10-20%)**: Manageable risk, plan carefully
- **High (>20%)**: Significant risk, consider closer markets

### Net Profit Calculation

```
Net Profit = (Price × Remaining Quantity) - Transport Cost

Where:
- Price = Predicted market price per kg
- Remaining Quantity = Initial Quantity × (1 - Spoilage Risk)
- Transport Cost = Distance × Rate × (Quantity/100) + Fixed Cost
```

**Example**:
```
Initial Quantity: 1000 kg
Price: ₹28.50/kg
Spoilage Risk: 5%
Transport Cost: ₹2,400

Remaining Quantity = 1000 × (1 - 0.05) = 950 kg
Revenue = ₹28.50 × 950 = ₹27,075
Net Profit = ₹27,075 - ₹2,400 = ₹24,675
```

---

## 🔌 API Usage

### Using the REST API Directly

#### 1. Get Market Recommendations

**Endpoint**: `POST /api/v1/predict`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "village_location": "theni",
    "crop_type": "tomato",
    "quantity_kg": 1000,
    "harvest_date": "2024-03-01"
  }'
```

**Response**:
```json
{
  "request_id": "req_20240225_123456_abc123",
  "timestamp": "2024-02-25T12:34:56",
  "village_location": "theni",
  "crop_type": "tomato",
  "quantity_kg": 1000,
  "markets": [
    {
      "market_id": "madurai",
      "market_name": "Madurai Mandi",
      "predicted_price": 28.5,
      "demand_level": "High",
      "spoilage_risk_percent": 5.2,
      "transport_cost": 2400.0,
      "net_profit": 20800.0,
      "confidence_score": 0.85,
      "optimal_selling_day": "2024-03-04",
      "distance_km": 80
    }
  ],
  "best_market": "Madurai Mandi",
  "best_market_id": "madurai",
  "explanation": "For 1,000 kg of tomatoes from Theni...",
  "total_markets_analyzed": 3,
  "forecast_days": 7
}
```

#### 2. Get Available Markets

**Endpoint**: `GET /api/v1/markets?location={village}&max_distance_km={distance}`

**Request**:
```bash
curl "http://localhost:8000/api/v1/markets?location=theni&max_distance_km=200"
```

#### 3. Get Supported Crops

**Endpoint**: `GET /api/v1/crops`

**Request**:
```bash
curl "http://localhost:8000/api/v1/crops"
```

#### 4. Get Specific Crop Details

**Endpoint**: `GET /api/v1/crops/{crop_id}`

**Request**:
```bash
curl "http://localhost:8000/api/v1/crops/tomato"
```

### API Documentation

Visit **http://localhost:8000/docs** for interactive API documentation with:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Example requests

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Backend won't start

**Solutions**:
```bash
# Check if virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt

# Check for port conflicts
# Try different port:
uvicorn main:app --port 8001
```

**Problem**: "Module not found" error

**Solution**:
```bash
# Ensure you're in backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verify Python path
which python  # Should point to venv
```

**Problem**: Database errors

**Solution**:
```bash
# Delete and recreate database
rm rpin.db  # Linux/Mac
del rpin.db  # Windows

# Restart server (will recreate database)
python main.py
```

### Frontend Issues

**Problem**: Frontend won't load

**Solutions**:
```bash
# Check if server is running
# Should see: Serving HTTP on 0.0.0.0 port 3000

# Try different port
python -m http.server 3001

# Or open index.html directly in browser
```

**Problem**: CORS errors

**Solution**:
- Backend CORS is already configured for localhost
- If using different ports, update ALLOWED_ORIGINS in backend/app/core/config.py

**Problem**: API connection failed

**Solutions**:
1. Verify backend is running: http://localhost:8000/health
2. Check API_BASE_URL in frontend/index.html
3. Check browser console for errors (F12)

### Application Issues

**Problem**: "Village not found" error

**Solution**:
- Use exact village names from dropdown
- Supported: theni, dindigul, salem, erode, namakkal, karur, tirupur, pollachi

**Problem**: "Crop not found" error

**Solution**:
- Use exact crop names from dropdown
- Supported: tomato, onion, potato, cabbage, carrot, cauliflower

**Problem**: No results returned

**Solutions**:
1. Check if harvest date is valid (today to 30 days future)
2. Verify quantity is reasonable (1-100,000 kg)
3. Check backend logs for errors
4. Try different village/crop combination

**Problem**: Unexpected results

**Explanation**:
- System uses mock data for demo
- Prices are generated based on trends and seasonality
- For production, integrate real AGMARKNET API

### Performance Issues

**Problem**: Slow response times

**Solutions**:
1. Check internet connection
2. Verify backend is not overloaded
3. Clear browser cache
4. Restart backend server

**Problem**: High memory usage

**Solution**:
```bash
# Restart backend
# Press CTRL+C to stop
# Then start again:
python main.py
```

---

## 📞 Support

### Getting Help

1. **Check Logs**:
   ```bash
   # Backend logs
   tail -f logs/rpin_*.log
   
   # Or check terminal output
   ```

2. **API Documentation**: http://localhost:8000/docs

3. **Test API Health**: http://localhost:8000/health

4. **Browser Console**: Press F12 to see JavaScript errors

### Common Questions

**Q: Can I use real API keys?**
A: Yes! Add your OpenWeather API key to `.env` file for real weather data.

**Q: How accurate are the predictions?**
A: For demo, uses simplified models. For production, train models on real historical data.

**Q: Can I add more villages/crops?**
A: Yes! Edit the JSON files in `backend/data/` directory.

**Q: How do I deploy to production?**
A: See AWS_DEPLOYMENT_GUIDE.md for complete deployment instructions.

**Q: Is the data real?**
A: Demo uses synthetic data. For production, integrate with real AGMARKNET API.

---

## 🎯 Best Practices

### For Farmers

1. **Plan Ahead**: Enter harvest date accurately
2. **Check Multiple Scenarios**: Try different dates to find optimal timing
3. **Consider All Factors**: Don't just look at price, consider distance and spoilage
4. **Verify Information**: Use as guidance, verify with local market conditions

### For Developers

1. **Keep Backend Running**: Don't stop during demos
2. **Monitor Logs**: Watch for errors
3. **Test Before Demo**: Run through complete workflow
4. **Have Backup**: Keep screenshots of working results

### For Hackathon

1. **Prepare Demo Scenarios**: Have 2-3 test cases ready
2. **Explain AI Components**: Highlight ML models used
3. **Show Social Impact**: Emphasize helping farmers
4. **Demonstrate Scalability**: Explain how it can grow

---

## ✅ Quick Reference

### Starting the Application

```bash
# Terminal 1 - Backend
cd backend && venv\Scripts\activate && python main.py

# Terminal 2 - Frontend
cd frontend && python -m http.server 3000

# Browser
http://localhost:3000
```

### Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Get prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"village_location":"theni","crop_type":"tomato","quantity_kg":1000,"harvest_date":"2024-03-01"}'
```

### Stopping the Application

```bash
# In each terminal, press:
CTRL+C
```

---

## 🎉 Success!

You're now ready to use RPIN to help farmers make better selling decisions!

**Remember**: This system helps farmers:
- 📈 Maximize profits
- 🎯 Find best markets
- ⏰ Choose optimal timing
- 📊 Make data-driven decisions
- 🌾 Reduce wastage

Happy farming! 🚜
