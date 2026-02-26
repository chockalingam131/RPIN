# RPIN Development Guide

## ✅ Completed Tasks

- **Task 1**: Project structure and core dependencies ✅
- **Task 2**: Data models and validation ✅
- **Task 3**: External data integration layer ✅

## 📦 What's Been Built

### 1. Core Infrastructure
- FastAPI application with CORS and lifespan management
- Configuration management with environment variables
- Logging system with file and console output
- Custom exception handling
- Database schema with SQLAlchemy

### 2. Data Models (Pydantic)
- **Domain Models**: Market, CropInfo, PriceData, WeatherData, VillageDistance, MarketRecommendation
- **Request Models**: PredictionRequest, MarketQueryRequest, CropQueryRequest
- **Response Models**: PredictionResponse, MarketListResponse, CropListResponse, ErrorResponse, HealthResponse

### 3. Data Layer
- **DataLoader**: Loads and caches JSON data files (crops, markets, distances)
- **Database**: SQLite with tables for historical prices, weather cache, user sessions, prediction logs
- **AGMARKNET Client**: Fetches mandi price data with caching and mock fallback
- **Weather Client**: Fetches weather forecasts with caching and mock fallback

### 4. Sample Data
- 6 crops with metadata
- 6 markets across Tamil Nadu
- 8 villages with distance data

## 🚀 Quick Start - Running the Application

### Step 1: Setup Environment

```bash
# Navigate to backend directory
cd backend

# Run setup script
# Windows:
setup.bat

# Linux/Mac:
chmod +x setup.sh
./setup.sh
```

### Step 2: Activate Virtual Environment

```bash
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Verify Setup

```bash
python test_setup.py
```

Expected output:
```
🎉 All tests passed! Setup is complete.
```

### Step 4: Run the Server

```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Test the API

Open your browser:
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 Testing the Data Layer

### Test Data Loading

Create a test script `test_data.py`:

```python
from app.data.loaders import data_loader
from app.data.agmarknet import agmarknet_client
from app.data.weather import weather_client

# Test crop loading
crops = data_loader.load_crops()
print(f"Loaded {len(crops)} crops")
print(f"Supported crops: {list(crops.keys())}")

# Test market loading
markets = data_loader.load_markets()
print(f"\nLoaded {len(markets)} markets")
print(f"Supported markets: {list(markets.keys())}")

# Test distance loading
distances = data_loader.load_distances()
print(f"\nLoaded {len(distances)} villages")
print(f"Supported villages: {list(distances.keys())}")

# Test getting nearby markets
nearby = data_loader.get_nearby_markets("theni", max_distance_km=200)
print(f"\nMarkets within 200km of Theni:")
for market_id, distance in nearby:
    print(f"  - {market_id}: {distance} km")

# Test price data (mock)
prices = agmarknet_client.fetch_historical_prices("tomato", "madurai", days=7)
print(f"\nFetched {len(prices)} price records for tomato in Madurai")
print(f"Latest price: ₹{prices[-1].modal_price}/kg")

# Test weather data (mock)
weather = weather_client.fetch_forecast("Madurai", days=7)
print(f"\nFetched {len(weather)} weather forecasts for Madurai")
print(f"Today's temperature: {weather[0].temperature_celsius}°C")
print(f"Today's humidity: {weather[0].humidity_percent}%")
```

Run it:
```bash
python test_data.py
```

### Test Request Validation

Create `test_validation.py`:

```python
from datetime import date, timedelta
from app.models.request import PredictionRequest
from pydantic import ValidationError

# Valid request
try:
    request = PredictionRequest(
        village_location="theni",
        crop_type="tomato",
        quantity_kg=1000,
        harvest_date=date.today() + timedelta(days=3)
    )
    print("✅ Valid request created")
    print(f"   Village: {request.village_location}")
    print(f"   Crop: {request.crop_type}")
    print(f"   Quantity: {request.quantity_kg} kg")
    print(f"   Harvest: {request.harvest_date}")
except ValidationError as e:
    print(f"❌ Validation error: {e}")

# Invalid request - past date
try:
    request = PredictionRequest(
        village_location="theni",
        crop_type="tomato",
        quantity_kg=1000,
        harvest_date=date.today() - timedelta(days=1)
    )
    print("❌ Should have failed validation")
except ValidationError as e:
    print("✅ Correctly rejected past date")

# Invalid request - negative quantity
try:
    request = PredictionRequest(
        village_location="theni",
        crop_type="tomato",
        quantity_kg=-100,
        harvest_date=date.today() + timedelta(days=3)
    )
    print("❌ Should have failed validation")
except ValidationError as e:
    print("✅ Correctly rejected negative quantity")
```

Run it:
```bash
python test_validation.py
```

## 📂 Project Structure

```
backend/
├── main.py                          # ✅ Application entry point
├── requirements.txt                 # ✅ Dependencies
├── .env.example                     # ✅ Environment template
├── setup.sh / setup.bat            # ✅ Setup scripts
├── test_setup.py                    # ✅ Setup verification
│
├── app/
│   ├── core/                        # ✅ Core components
│   │   ├── config.py                # ✅ Settings
│   │   ├── logging.py               # ✅ Logging
│   │   └── exceptions.py            # ✅ Exceptions
│   │
│   ├── models/                      # ✅ Pydantic models
│   │   ├── domain.py                # ✅ Domain models
│   │   ├── request.py               # ✅ Request models
│   │   └── response.py              # ✅ Response models
│   │
│   ├── data/                        # ✅ Data access layer
│   │   ├── loaders.py               # ✅ JSON data loader
│   │   ├── database.py              # ✅ SQLite database
│   │   ├── agmarknet.py             # ✅ Price data client
│   │   └── weather.py               # ✅ Weather client
│   │
│   ├── api/v1/                      # ⏭️ API endpoints (Task 9)
│   ├── services/                    # ⏭️ Business logic (Tasks 5-7)
│   └── ml/                          # ⏭️ ML models (Task 5)
│
└── data/                            # ✅ Static data files
    ├── crops.json                   # ✅ 6 crops
    ├── markets.json                 # ✅ 6 markets
    └── distances.json               # ✅ 8 villages
```

## 🔄 Next Steps

### Task 4: Checkpoint (Optional)
Run tests to ensure data layer works correctly.

### Task 5: Implement ML Prediction Models
**Priority for MVP:**
- 5.1: Price prediction service (XGBoost or simplified model)
- 5.3: Demand classification service
- 5.4: Spoilage risk predictor

**Files to create:**
- `app/ml/price_predictor.py`
- `app/ml/demand_classifier.py`
- `app/ml/spoilage_predictor.py`

### Task 6: Transport and Optimization Services
- 6.1: Transport cost calculator
- 6.3: Profit optimization engine

**Files to create:**
- `app/services/optimization.py`

### Task 7: Explanation Generation
- 7.1: LLM integration for explanations

**Files to create:**
- `app/services/explanation.py`

### Task 9: FastAPI REST Endpoints
- 9.1: Main prediction endpoint
- 9.2: Supporting endpoints (markets, crops, health)

**Files to create:**
- `app/api/v1/endpoints/prediction.py`
- `app/api/v1/endpoints/markets.py`
- `app/api/v1/endpoints/crops.py`

### Task 10: React Frontend
- Set up React application
- Create input form
- Create results display

## 🛠️ Development Workflow

### 1. Start Development Server
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

Server runs at: http://localhost:8000

### 2. Make Code Changes
Edit files in `app/` directory. Server auto-reloads with `--reload` flag.

### 3. Test Changes
- Visit http://localhost:8000/docs for interactive API testing
- Check logs in `logs/` directory
- Run test scripts

### 4. Check Logs
```bash
# View latest log file
# Windows:
type logs\rpin_*.log

# Linux/Mac:
tail -f logs/rpin_*.log
```

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
# Check with:
which python  # Linux/Mac
where python  # Windows

# Should point to venv/bin/python or venv\Scripts\python
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Database Errors
```bash
# Delete and recreate database
rm rpin.db
python main.py  # Will recreate on startup
```

### Data Loading Errors
```bash
# Verify data files exist
ls data/  # Linux/Mac
dir data\  # Windows

# Should see: crops.json, markets.json, distances.json
```

## 📊 API Testing Examples

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/
```

### Using Python requests

```python
import requests
from datetime import date, timedelta

# Test prediction endpoint (once implemented)
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "village_location": "theni",
        "crop_type": "tomato",
        "quantity_kg": 1000,
        "harvest_date": str(date.today() + timedelta(days=3))
    }
)
print(response.json())
```

## 🔐 Environment Variables

Edit `.env` file:

```env
# Required for full functionality
OPENWEATHER_API_KEY=your_key_here
LLM_API_KEY=your_key_here

# Optional - defaults work for development
DATABASE_URL=sqlite:///./rpin.db
LOG_LEVEL=INFO
FORECAST_DAYS=7
```

### Getting API Keys

**OpenWeather API (Free)**:
1. Sign up at https://openweathermap.org/api
2. Get API key from dashboard
3. Add to `.env`: `OPENWEATHER_API_KEY=your_key`

**LLM API (Optional for MVP)**:
- OpenAI: https://platform.openai.com/api-keys
- Or use template-based explanations initially

## 📈 Performance Tips

### 1. Enable Caching
Caching is enabled by default for:
- Static data (crops, markets, distances)
- Price data (24-hour TTL)
- Weather data (6-hour TTL)

### 2. Monitor Logs
```bash
tail -f logs/rpin_*.log
```

### 3. Database Optimization
For production, consider PostgreSQL instead of SQLite.

## 🎯 MVP Development Priority

For hackathon demo, focus on:

1. ✅ **Core infrastructure** (Done)
2. ✅ **Data models** (Done)
3. ✅ **Data integration** (Done)
4. ⏭️ **ML models** (Task 5) - Use simplified models
5. ⏭️ **Optimization** (Task 6) - Core profit calculation
6. ⏭️ **API endpoints** (Task 9) - Main prediction endpoint
7. ⏭️ **Frontend** (Task 10) - Basic UI

Skip optional tasks marked with `*` in tasks.md for faster MVP.

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Project Spec**: `.kiro/specs/rural-producer-intelligence-network/`

## 🤝 Need Help?

- Check `QUICKSTART.md` for hackathon-specific guidance
- Check `PROJECT_STRUCTURE.md` for detailed file descriptions
- Review spec files in `.kiro/specs/rural-producer-intelligence-network/`
- Check logs in `logs/` directory

Happy coding! 🚀
