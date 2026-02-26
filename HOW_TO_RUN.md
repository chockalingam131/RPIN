# How to Run RPIN - Quick Reference

## 🎯 For First-Time Setup

### Windows

```bash
# 1. Navigate to backend
cd backend

# 2. Run setup script
setup.bat

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Verify setup
python test_setup.py

# 5. Run server
python main.py
```

### Linux/Mac

```bash
# 1. Navigate to backend
cd backend

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Verify setup
python test_setup.py

# 5. Run server
python main.py
```

## 🚀 For Daily Development

### Start the Server

```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run server
python main.py
```

Server will start at: **http://localhost:8000**

### Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

## 📦 What's Currently Working

### ✅ Completed Features

1. **Core Infrastructure**
   - FastAPI application running
   - Configuration management
   - Logging system
   - Error handling

2. **Data Models**
   - Request/Response validation
   - Domain models (Market, Crop, Weather, etc.)
   - Automatic API documentation

3. **Data Layer**
   - JSON data loading (crops, markets, distances)
   - SQLite database
   - Price data client (with mock data)
   - Weather client (with mock data)

### 🔄 What You Can Test Now

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "RPIN - Rural Producer Intelligence Network",
  "version": "1.0.0"
}
```

#### 2. Root Endpoint
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Welcome to RPIN - Rural Producer Intelligence Network",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### 3. Interactive API Docs
Open browser: http://localhost:8000/docs

You'll see:
- Swagger UI with all available endpoints
- Try out API calls directly from browser
- View request/response schemas

## 🧪 Testing the Data Layer

Create a file `test_data.py` in the backend directory:

```python
from app.data.loaders import data_loader
from app.data.agmarknet import agmarknet_client
from app.data.weather import weather_client

print("=" * 60)
print("RPIN Data Layer Test")
print("=" * 60)

# Test 1: Load crops
print("\n1. Loading crops...")
crops = data_loader.load_crops()
print(f"   ✅ Loaded {len(crops)} crops")
print(f"   Crops: {', '.join(crops.keys())}")

# Test 2: Load markets
print("\n2. Loading markets...")
markets = data_loader.load_markets()
print(f"   ✅ Loaded {len(markets)} markets")
print(f"   Markets: {', '.join(markets.keys())}")

# Test 3: Load distances
print("\n3. Loading village distances...")
distances = data_loader.load_distances()
print(f"   ✅ Loaded {len(distances)} villages")
print(f"   Villages: {', '.join(distances.keys())}")

# Test 4: Get nearby markets
print("\n4. Finding markets near Theni (within 200km)...")
nearby = data_loader.get_nearby_markets("theni", max_distance_km=200)
for market_id, distance in nearby:
    market = data_loader.get_market(market_id)
    print(f"   - {market.name}: {distance} km")

# Test 5: Fetch price data
print("\n5. Fetching price data for tomato in Madurai...")
prices = agmarknet_client.fetch_historical_prices("tomato", "madurai", days=7)
print(f"   ✅ Fetched {len(prices)} price records")
print(f"   Latest price: ₹{prices[-1].modal_price}/kg on {prices[-1].date}")

# Test 6: Fetch weather data
print("\n6. Fetching weather forecast for Madurai...")
weather = weather_client.fetch_forecast("Madurai", days=7)
print(f"   ✅ Fetched {len(weather)} weather forecasts")
print(f"   Today: {weather[0].temperature_celsius}°C, {weather[0].humidity_percent}% humidity")

print("\n" + "=" * 60)
print("All tests passed! ✅")
print("=" * 60)
```

Run it:
```bash
python test_data.py
```

## 📁 Project Files Overview

```
backend/
├── main.py                    # ✅ Start server here
├── requirements.txt           # ✅ Dependencies
├── .env                       # ✅ Configuration (create from .env.example)
├── setup.sh / setup.bat      # ✅ Setup scripts
├── test_setup.py             # ✅ Verify installation
├── test_data.py              # 🆕 Test data layer (create this)
│
├── app/                       # Application code
│   ├── core/                 # ✅ Config, logging, exceptions
│   ├── models/               # ✅ Pydantic models
│   ├── data/                 # ✅ Data access layer
│   ├── api/                  # ⏭️ API endpoints (Task 9)
│   ├── services/             # ⏭️ Business logic (Tasks 5-7)
│   └── ml/                   # ⏭️ ML models (Task 5)
│
├── data/                      # ✅ Static data
│   ├── crops.json            # ✅ 6 crops
│   ├── markets.json          # ✅ 6 markets
│   └── distances.json        # ✅ 8 villages
│
├── logs/                      # 📝 Application logs
└── rpin.db                    # 💾 SQLite database (auto-created)
```

## 🔧 Common Commands

### Start Server
```bash
python main.py
```

### Start with Auto-Reload
```bash
uvicorn main:app --reload
```

### Start on Different Port
```bash
uvicorn main:app --reload --port 8001
```

### View Logs
```bash
# Windows:
type logs\rpin_*.log

# Linux/Mac:
tail -f logs/rpin_*.log
```

### Clear Database
```bash
# Windows:
del rpin.db

# Linux/Mac:
rm rpin.db

# Then restart server to recreate
python main.py
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### "Module not found" Error
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal prompt

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### "Port already in use" Error
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### "Permission denied" on setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

### Data Files Not Found
```bash
# Verify data files exist
# Windows:
dir data

# Linux/Mac:
ls -la data

# Should see: crops.json, markets.json, distances.json
```

## 📊 Expected Output When Starting Server

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
2024-02-25 12:00:00 - app.data.database - INFO - Database tables created successfully
2024-02-25 12:00:00 - app.data.loaders - INFO - Loaded 6 crops
2024-02-25 12:00:00 - app.data.loaders - INFO - Loaded 6 markets
2024-02-25 12:00:00 - app.data.loaders - INFO - Loaded 8 villages
2024-02-25 12:00:00 - __main__ - INFO - Starting RPIN application...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🎯 Next Development Steps

After confirming everything works:

1. **Task 5**: Implement ML prediction models
   - Price predictor
   - Demand classifier
   - Spoilage predictor

2. **Task 6**: Implement optimization services
   - Transport cost calculator
   - Profit optimization engine

3. **Task 7**: Implement explanation generation
   - LLM integration or template-based

4. **Task 9**: Implement API endpoints
   - POST /api/v1/predict
   - GET /api/v1/markets/{location}
   - GET /api/v1/crops

5. **Task 10**: Build React frontend
   - Input form
   - Results table
   - Explanation panel

## 📚 Documentation

- **DEVELOPMENT_GUIDE.md** - Detailed development guide
- **QUICKSTART.md** - Hackathon quick start
- **PROJECT_STRUCTURE.md** - Complete project structure
- **backend/README.md** - Backend-specific docs
- **.kiro/specs/** - Complete specifications

## 🆘 Need Help?

1. Check if server is running: http://localhost:8000/health
2. Check logs in `logs/` directory
3. Run `python test_setup.py` to verify installation
4. Review error messages in terminal
5. Check `.env` file configuration

## ✅ Quick Checklist

Before starting development:
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows fastapi, uvicorn, etc.)
- [ ] `.env` file created (copy from `.env.example`)
- [ ] Data files exist in `data/` directory
- [ ] Server starts without errors
- [ ] http://localhost:8000/docs loads successfully
- [ ] `test_data.py` runs successfully

If all checked, you're ready to continue development! 🚀
