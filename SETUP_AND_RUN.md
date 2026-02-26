# RPIN - Complete Setup and Run Guide

## 📋 What Has Been Built

### ✅ Completed Tasks (1-3)

**Task 1: Project Structure** ✅
- FastAPI application with CORS and lifespan management
- Configuration system with environment variables
- Logging infrastructure (file + console)
- Custom exception handling
- Setup scripts for Windows and Linux/Mac

**Task 2: Data Models** ✅
- Domain models: Market, CropInfo, PriceData, WeatherData, VillageDistance, MarketRecommendation
- Request models: PredictionRequest, MarketQueryRequest, CropQueryRequest
- Response models: PredictionResponse, MarketListResponse, CropListResponse, ErrorResponse
- Full validation with Pydantic

**Task 3: Data Integration** ✅
- DataLoader: Loads and caches JSON data (crops, markets, distances)
- Database: SQLite with tables for prices, weather, sessions, logs
- AGMARKNET Client: Fetches mandi price data (with mock fallback)
- Weather Client: Fetches weather forecasts (with mock fallback)

### 📊 Sample Data Included

- **6 Crops**: tomato, onion, potato, cabbage, carrot, cauliflower
- **6 Markets**: Madurai, Chennai, Coimbatore, Trichy, Salem, Erode
- **8 Villages**: Theni, Dindigul, Salem, Erode, Namakkal, Karur, Tirupur, Pollachi

---

## 🚀 STEP-BY-STEP SETUP

### Step 1: Initial Setup (One-Time)

#### On Windows:

```bash
# Navigate to backend directory
cd backend

# Run setup script
setup.bat

# This will:
# - Create virtual environment
# - Install all dependencies
# - Create .env file
# - Create necessary directories
```

#### On Linux/Mac:

```bash
# Navigate to backend directory
cd backend

# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh

# This will:
# - Create virtual environment
# - Install all dependencies
# - Create .env file
# - Create necessary directories
```

### Step 2: Verify Installation

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Run verification script
python test_setup.py
```

**Expected Output:**
```
============================================================
RPIN Backend Setup Verification
============================================================

Testing package imports...
  ✓ fastapi
  ✓ uvicorn
  ✓ pydantic
  ✓ pandas
  ✓ numpy
  ✓ sklearn
  ✓ xgboost
  ✓ requests
  ✓ sqlalchemy

✅ All packages imported successfully!

Testing directory structure...
  ✓ app/
  ✓ app/core/
  ✓ app/api/
  ✓ app/models/
  ✓ app/services/
  ✓ app/ml/
  ✓ app/data/
  ✓ data/

✅ All directories exist!

Testing data files...
  ✓ data/crops.json
  ✓ data/markets.json
  ✓ data/distances.json

✅ All data files exist!

Testing configuration...
  ✓ Project: RPIN - Rural Producer Intelligence Network
  ✓ Version: 1.0.0
  ✓ API Prefix: /api/v1

✅ Configuration loaded successfully!

============================================================
🎉 All tests passed! Setup is complete.
============================================================
```

### Step 3: Test Data Layer

```bash
# Still in backend directory with venv activated
python test_data.py
```

**Expected Output:**
```
============================================================
RPIN Data Layer Test
============================================================

1. Loading crops...
   ✅ Loaded 6 crops
   Crops: tomato, onion, potato, cabbage, carrot, cauliflower
   Example - Tomato: 7 days shelf life

2. Loading markets...
   ✅ Loaded 6 markets
   Markets: madurai, chennai, coimbatore, trichy, salem, erode
   Example - Madurai Mandi: 500 tons capacity

3. Loading village distances...
   ✅ Loaded 8 villages
   Villages: theni, dindigul, salem, erode, namakkal, karur, tirupur, pollachi

4. Finding markets near Theni (within 200km)...
   ✅ Found 5 nearby markets:
      - Madurai Mandi: 80 km
      - Coimbatore Market: 180 km
      - Trichy Mandi: 200 km

5. Fetching price data for tomato in Madurai...
   ✅ Fetched 7 price records
   Latest price: ₹27.35/kg on 2024-02-25
   Price range: ₹24.12 - ₹30.58

6. Fetching weather forecast for Madurai...
   ✅ Fetched 7 weather forecasts
   Today: 31.2°C, 68.5% humidity
   Tomorrow: 29.8°C, 72.1% humidity

7. Testing data queries...
   ✅ All queries working correctly
   Distance Theni → Madurai: 80 km

============================================================
🎉 All tests passed! Data layer is working correctly.
============================================================
```

### Step 4: Start the Server

```bash
# Make sure you're in backend directory with venv activated
python main.py
```

**Expected Output:**
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
INFO:     Started reloader process [12346] using StatReload
```

### Step 5: Test the API

Open your browser and visit:

1. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI
   - Try out API calls
   - View request/response schemas

2. **Alternative Docs**: http://localhost:8000/redoc
   - Clean, readable documentation

3. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy", ...}`

4. **Root Endpoint**: http://localhost:8000/
   - Welcome message

---

## 🔄 DAILY DEVELOPMENT WORKFLOW

### Starting Development

```bash
# 1. Navigate to backend
cd backend

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Start server
python main.py
```

### Making Changes

1. Edit files in `app/` directory
2. Server auto-reloads (if using `--reload` flag)
3. Test changes at http://localhost:8000/docs
4. Check logs in `logs/` directory

### Stopping the Server

Press `CTRL+C` in the terminal

---

## 📁 PROJECT STRUCTURE

```
backend/
├── main.py                          # ✅ Start here
├── requirements.txt                 # ✅ Dependencies
├── .env                             # ✅ Configuration
├── setup.sh / setup.bat            # ✅ Setup scripts
├── test_setup.py                    # ✅ Verify installation
├── test_data.py                     # ✅ Test data layer
│
├── app/
│   ├── core/                        # ✅ Config, logging, exceptions
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   │
│   ├── models/                      # ✅ Pydantic models
│   │   ├── domain.py                # Business entities
│   │   ├── request.py               # API requests
│   │   └── response.py              # API responses
│   │
│   ├── data/                        # ✅ Data access
│   │   ├── loaders.py               # JSON data loader
│   │   ├── database.py              # SQLite database
│   │   ├── agmarknet.py             # Price data client
│   │   └── weather.py               # Weather client
│   │
│   ├── api/v1/                      # ⏭️ API endpoints (Task 9)
│   ├── services/                    # ⏭️ Business logic (Tasks 5-7)
│   └── ml/                          # ⏭️ ML models (Task 5)
│
├── data/                            # ✅ Static data
│   ├── crops.json
│   ├── markets.json
│   └── distances.json
│
├── logs/                            # 📝 Application logs
├── models/                          # 🤖 ML model files (Task 5)
└── rpin.db                          # 💾 SQLite database
```

---

## 🧪 TESTING COMMANDS

### Test Installation
```bash
python test_setup.py
```

### Test Data Layer
```bash
python test_data.py
```

### Test API (using curl)
```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/
```

### View Logs
```bash
# Windows:
type logs\rpin_*.log

# Linux/Mac:
tail -f logs/rpin_*.log
```

---

## 🐛 TROUBLESHOOTING

### Problem: "Module not found" error

**Solution:**
```bash
# Ensure virtual environment is activated
# You should see (venv) in your prompt

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Verify:
which python  # Should point to venv/bin/python
```

### Problem: "Port already in use"

**Solution:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Problem: Data files not found

**Solution:**
```bash
# Verify files exist
ls data/  # Linux/Mac
dir data\  # Windows

# Should see: crops.json, markets.json, distances.json
```

### Problem: Permission denied on setup.sh

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Problem: Database errors

**Solution:**
```bash
# Delete and recreate database
rm rpin.db  # Linux/Mac
del rpin.db  # Windows

# Restart server (will recreate database)
python main.py
```

---

## ⏭️ NEXT STEPS

After confirming everything works, continue with:

### Task 5: ML Prediction Models
- Price predictor (XGBoost or simplified)
- Demand classifier (RandomForest or rule-based)
- Spoilage risk calculator

### Task 6: Optimization Services
- Transport cost calculator
- Profit optimization engine

### Task 7: Explanation Generation
- LLM integration or template-based

### Task 9: API Endpoints
- POST /api/v1/predict
- GET /api/v1/markets/{location}
- GET /api/v1/crops

### Task 10: React Frontend
- Input form
- Results table
- Explanation panel

---

## 📚 DOCUMENTATION

| File | Purpose |
|------|---------|
| **README.md** | Project overview and quick start |
| **HOW_TO_RUN.md** | Quick reference guide |
| **DEVELOPMENT_GUIDE.md** | Detailed development guide |
| **QUICKSTART.md** | Hackathon rapid development |
| **PROJECT_STRUCTURE.md** | Complete file structure |
| **SETUP_AND_RUN.md** | This file - complete setup guide |

---

## ✅ QUICK CHECKLIST

Before continuing development:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] `.env` file created
- [ ] `python test_setup.py` passes
- [ ] `python test_data.py` passes
- [ ] Server starts without errors
- [ ] http://localhost:8000/docs loads
- [ ] Health check returns "healthy"

If all checked, you're ready! 🚀

---

## 🆘 NEED HELP?

1. **Check server status**: http://localhost:8000/health
2. **Check logs**: `logs/rpin_*.log`
3. **Verify setup**: `python test_setup.py`
4. **Test data**: `python test_data.py`
5. **Review docs**: Check other .md files in project root

---

## 🎯 CURRENT CAPABILITIES

What you can do right now:

✅ Load crop information (6 crops)
✅ Load market information (6 markets)
✅ Load village distances (8 villages)
✅ Find nearby markets for a village
✅ Fetch historical price data (mock)
✅ Fetch weather forecasts (mock)
✅ Validate API requests
✅ Access interactive API documentation

What's coming next:

⏭️ ML-powered price predictions
⏭️ Demand classification
⏭️ Spoilage risk calculation
⏭️ Profit optimization
⏭️ Complete REST API
⏭️ React web interface

---

## 🚀 START DEVELOPING NOW!

```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python main.py
```

Then open: **http://localhost:8000/docs**

Happy coding! 🎉
