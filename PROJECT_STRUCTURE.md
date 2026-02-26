# RPIN Project Structure

## Overview

This document describes the complete project structure for the Rural Producer Intelligence Network (RPIN) system.

## Directory Structure

```
rpin-prototype/
├── backend/                          # FastAPI backend application
│   ├── main.py                       # Application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   ├── .env                          # Environment variables (create from .env.example)
│   ├── .gitignore                    # Git ignore rules
│   ├── README.md                     # Backend documentation
│   ├── setup.sh                      # Setup script for Linux/Mac
│   ├── setup.bat                     # Setup script for Windows
│   ├── test_setup.py                 # Setup verification script
│   │
│   ├── app/                          # Application package
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                     # Core configuration and utilities
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Settings and configuration
│   │   │   ├── logging.py            # Logging configuration
│   │   │   └── exceptions.py         # Custom exceptions
│   │   │
│   │   ├── api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── v1/                   # API version 1
│   │   │       ├── __init__.py
│   │   │       └── endpoints/        # Endpoint modules (Task 9)
│   │   │           ├── prediction.py
│   │   │           ├── markets.py
│   │   │           └── crops.py
│   │   │
│   │   ├── models/                   # Pydantic models (Task 2)
│   │   │   ├── __init__.py
│   │   │   ├── request.py            # Request models
│   │   │   ├── response.py           # Response models
│   │   │   └── domain.py             # Domain models
│   │   │
│   │   ├── services/                 # Business logic (Tasks 5-7)
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py         # Prediction orchestration
│   │   │   ├── optimization.py       # Profit optimization
│   │   │   └── explanation.py        # LLM explanation generation
│   │   │
│   │   ├── ml/                       # ML models (Task 5)
│   │   │   ├── __init__.py
│   │   │   ├── price_predictor.py    # XGBoost price prediction
│   │   │   ├── demand_classifier.py  # RandomForest demand classification
│   │   │   └── spoilage_predictor.py # Spoilage risk calculation
│   │   │
│   │   └── data/                     # Data access layer (Task 3)
│   │       ├── __init__.py
│   │       ├── loaders.py            # Data loading utilities
│   │       ├── agmarknet.py          # AGMARKNET API client
│   │       └── weather.py            # Weather API client
│   │
│   ├── data/                         # Static data files
│   │   ├── crops.json                # Crop information
│   │   ├── markets.json              # Market information
│   │   └── distances.json            # Village-to-market distances
│   │
│   ├── models/                       # Trained ML models (Task 5)
│   │   ├── price_model.pkl
│   │   ├── demand_model.pkl
│   │   └── spoilage_model.pkl
│   │
│   ├── logs/                         # Application logs
│   │   └── rpin_YYYYMMDD.log
│   │
│   └── tests/                        # Test files (Tasks 2.2, 5.2, etc.)
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_services.py
│       └── test_api.py
│
├── frontend/                         # React frontend (Task 10)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputForm.tsx
│   │   │   ├── ResultsTable.tsx
│   │   │   └── ExplanationPanel.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── README.md
│
├── .kiro/                            # Kiro spec files
│   └── specs/
│       └── rural-producer-intelligence-network/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
│
├── architecture-diagram.md           # Architecture diagrams
├── QUICKSTART.md                     # Quick start guide
└── PROJECT_STRUCTURE.md              # This file
```

## File Descriptions

### Backend Core Files

- **main.py**: FastAPI application entry point with CORS, lifespan events, and route registration
- **requirements.txt**: All Python package dependencies
- **.env.example**: Template for environment variables
- **setup.sh/bat**: Automated setup scripts for different platforms
- **test_setup.py**: Verification script to test setup completion

### Application Modules

#### Core (`app/core/`)
- **config.py**: Centralized configuration using Pydantic Settings
- **logging.py**: Logging setup with file and console handlers
- **exceptions.py**: Custom exception classes for error handling

#### API (`app/api/v1/`)
- **endpoints/prediction.py**: Main prediction endpoint (POST /api/v1/predict)
- **endpoints/markets.py**: Market information endpoints
- **endpoints/crops.py**: Crop information endpoints

#### Models (`app/models/`)
- **request.py**: Request validation models (PredictionRequest, etc.)
- **response.py**: Response models (PredictionResponse, MarketRecommendation)
- **domain.py**: Domain models (Market, CropInfo, PriceData, WeatherData)

#### Services (`app/services/`)
- **prediction.py**: Orchestrates all prediction services
- **optimization.py**: Profit calculation and market ranking
- **explanation.py**: Natural language explanation generation

#### ML (`app/ml/`)
- **price_predictor.py**: XGBoost model for price forecasting
- **demand_classifier.py**: RandomForest model for demand classification
- **spoilage_predictor.py**: Regression model for spoilage risk

#### Data (`app/data/`)
- **loaders.py**: Utilities to load JSON data files
- **agmarknet.py**: Client for AGMARKNET API
- **weather.py**: Client for OpenWeather API

### Data Files

- **crops.json**: Crop metadata (shelf life, optimal temperature, handling)
- **markets.json**: Market information (location, capacity, operating days)
- **distances.json**: Pre-calculated distances between villages and markets

## Task Mapping

| Task | Files Created | Description |
|------|---------------|-------------|
| 1 | Core structure, config, logging | ✅ Completed |
| 2.1 | app/models/*.py | Pydantic models |
| 2.3 | app/data/loaders.py | Database and data loading |
| 3.1 | app/data/agmarknet.py | AGMARKNET client |
| 3.2 | app/data/weather.py | Weather API client |
| 5.1 | app/ml/price_predictor.py | Price prediction model |
| 5.3 | app/ml/demand_classifier.py | Demand classification |
| 5.4 | app/ml/spoilage_predictor.py | Spoilage risk predictor |
| 6.1 | app/services/optimization.py | Transport cost calculator |
| 6.3 | app/services/optimization.py | Profit optimization |
| 7.1 | app/services/explanation.py | LLM explanation service |
| 9.1 | app/api/v1/endpoints/prediction.py | Main API endpoint |
| 9.2 | app/api/v1/endpoints/*.py | Supporting endpoints |
| 10 | frontend/* | React application |

## Getting Started

### Backend Setup

```bash
cd backend

# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat

# Verify setup
python test_setup.py

# Run server
python main.py
```

### Frontend Setup (Task 10)

```bash
cd frontend
npm install
npm start
```

## API Endpoints (After Task 9)

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/predict` - Main prediction endpoint
- `GET /api/v1/markets/{location}` - Get markets for location
- `GET /api/v1/crops` - Get supported crops
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Environment Variables

See `.env.example` for all available configuration options.

Required for full functionality:
- `OPENWEATHER_API_KEY` - OpenWeather API key
- `LLM_API_KEY` - LLM API key (OpenAI, etc.)

## Next Steps

1. ✅ Task 1 completed - Project structure set up
2. ⏭️ Task 2 - Implement data models and validation
3. ⏭️ Task 3 - Implement external data integration
4. ⏭️ Task 5 - Implement ML prediction models

Refer to `.kiro/specs/rural-producer-intelligence-network/tasks.md` for detailed task descriptions.
