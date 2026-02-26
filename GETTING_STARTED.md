# Getting Started with RPIN Development

## ✅ Task 1 Complete!

The project structure and core dependencies have been set up successfully.

## What Was Created

### Backend Structure
```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment configuration template
├── setup.sh / setup.bat      # Automated setup scripts
├── test_setup.py             # Setup verification
├── app/
│   ├── core/                 # Configuration, logging, exceptions
│   ├── api/v1/              # API endpoints (ready for Task 9)
│   ├── models/              # Pydantic models (ready for Task 2)
│   ├── services/            # Business logic (ready for Tasks 5-7)
│   ├── ml/                  # ML models (ready for Task 5)
│   └── data/                # Data access (ready for Task 3)
└── data/
    ├── crops.json           # 6 crops with metadata
    ├── markets.json         # 6 markets in Tamil Nadu
    └── distances.json       # 8 villages with distances
```

### Configuration Files
- ✅ FastAPI application with CORS and lifespan management
- ✅ Centralized settings using Pydantic Settings
- ✅ Logging configuration with file and console output
- ✅ Custom exception classes for error handling
- ✅ Environment variable management

### Sample Data
- ✅ 6 crops: tomato, onion, potato, cabbage, carrot, cauliflower
- ✅ 6 markets: Madurai, Chennai, Coimbatore, Trichy, Salem, Erode
- ✅ 8 villages with distance data to all markets

## Quick Start

### Step 1: Navigate to Backend

```bash
cd backend
```

### Step 2: Run Setup Script

**On Windows:**
```bash
setup.bat
```

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual Setup (if scripts don't work):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Step 3: Configure Environment

Edit `.env` file and add your API keys:
```env
OPENWEATHER_API_KEY=your_key_here
LLM_API_KEY=your_key_here
```

**Note:** For initial development, you can leave these empty and use mock data.

### Step 4: Verify Setup

```bash
python test_setup.py
```

You should see:
```
🎉 All tests passed! Setup is complete.
```

### Step 5: Run the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

### Step 6: Test the API

Open your browser and visit:
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You should see the welcome message and API documentation.

## What's Next?

### Task 2: Implement Data Models (Next Step)

Create Pydantic models for:
- Request validation (PredictionRequest)
- Response formatting (PredictionResponse, MarketRecommendation)
- Domain models (Market, CropInfo, PriceData, WeatherData)

**Files to create:**
- `backend/app/models/request.py`
- `backend/app/models/response.py`
- `backend/app/models/domain.py`

### Task 3: External Data Integration

Implement API clients for:
- AGMARKNET mandi price data
- OpenWeather API for weather forecasts
- Data loading utilities for JSON files

### Task 5: ML Models

Implement prediction models:
- XGBoost for price prediction
- RandomForest for demand classification
- Regression for spoilage risk

## Development Workflow

1. **Start the server** with `python main.py`
2. **Make changes** to code files
3. **Server auto-reloads** (if using --reload flag)
4. **Test changes** at http://localhost:8000/docs
5. **Check logs** in `logs/` directory

## Troubleshooting

### Import Errors
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in main.py or use:
uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Make sure you're in the backend directory
cd backend

# Check Python path
python -c "import sys; print(sys.path)"
```

## Project Documentation

- **QUICKSTART.md** - Rapid prototype development guide
- **PROJECT_STRUCTURE.md** - Complete project structure documentation
- **architecture-diagram.md** - System architecture diagrams
- **backend/README.md** - Backend-specific documentation
- **.kiro/specs/** - Complete specification documents

## API Keys (Optional for MVP)

For the hackathon prototype, you can develop without external APIs initially:

1. **OpenWeather API** (Free tier)
   - Sign up: https://openweathermap.org/api
   - Get API key from dashboard
   - Add to `.env`: `OPENWEATHER_API_KEY=your_key`

2. **LLM API** (OpenAI or alternatives)
   - OpenAI: https://platform.openai.com/api-keys
   - Or use local LLM or template-based explanations
   - Add to `.env`: `LLM_API_KEY=your_key`

3. **AGMARKNET** (Public data)
   - No API key required
   - Use synthetic data for prototype

## Testing the Setup

### Test 1: Check Server Response
```bash
curl http://localhost:8000/
```

Expected output:
```json
{
  "message": "Welcome to RPIN - Rural Producer Intelligence Network",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Test 2: Check Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "service": "RPIN - Rural Producer Intelligence Network",
  "version": "1.0.0"
}
```

### Test 3: Check Data Files
```bash
# Windows:
type data\crops.json
# Linux/Mac:
cat data/crops.json
```

Should display crop information in JSON format.

## Ready to Continue?

Task 1 is complete! You now have:
- ✅ Complete project structure
- ✅ FastAPI application running
- ✅ Configuration management
- ✅ Logging infrastructure
- ✅ Sample data files
- ✅ Development environment

**Next:** Proceed to Task 2 to implement data models and validation.

Run this command to start Task 2:
```bash
# From the project root
# Tell Kiro: "Start Task 2"
```

## Questions?

- Check **PROJECT_STRUCTURE.md** for detailed file descriptions
- Check **QUICKSTART.md** for hackathon-specific guidance
- Check **backend/README.md** for backend documentation
- Review the spec files in `.kiro/specs/rural-producer-intelligence-network/`

Happy coding! 🚀
