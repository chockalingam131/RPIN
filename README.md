# RPIN - Rural Producer Intelligence Network

AI-powered market recommendation system for rural producers to maximize profit and minimize wastage.

## 🎯 Project Overview

RPIN helps rural producers (farmers, small-scale growers, artisans) make informed selling decisions by providing intelligent recommendations on:
- **What to sell**: Crop type and quantity
- **Where to sell**: Best market selection
- **When to sell**: Optimal selling day
- **Expected price**: Profit maximization

## 🏆 Hackathon Theme

**AI for Rural Innovation & Sustainable Systems**

## ✅ Current Status: READY TO DEPLOY

### All Features Complete! 🎉

- ✅ **Core Infrastructure**: FastAPI application with configuration, logging, and error handling
- ✅ **Data Models**: Pydantic models for validation and API documentation
- ✅ **Data Layer**: JSON data loading, SQLite database, external API clients
- ✅ **ML Models**: Price prediction, demand classification, spoilage risk assessment
- ✅ **Optimization**: Transport cost calculation, profit optimization engine
- ✅ **API Endpoints**: Complete REST API with interactive documentation
- ✅ **Frontend**: Responsive web interface with HTML/JavaScript
- ✅ **Sample Data**: 6 crops, 6 markets, 8 villages with distances
- ✅ **Documentation**: Complete guides for usage and deployment
- ✅ **Vercel Ready**: Configured for instant deployment

## 🚀 Deploy to Vercel (Recommended)

### Quick Deploy - No Python Installation Required!

**Option 1: Automated Script (Windows)**
```bash
deploy.bat
```

**Option 2: Automated Script (Linux/Mac)**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Option 3: Manual Steps**
1. Push to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Click "Deploy"
5. Done! ✅

**📖 Detailed Guide:** See [DEPLOY_NOW.md](DEPLOY_NOW.md)

## 🖥️ Run Locally (Optional)

### Prerequisites

- Python 3.9+
- Git

### Setup & Run

```bash
# 1. Navigate to backend
cd backend

# 2. Run setup script
# Windows: setup.bat
# Linux/Mac: ./setup.sh

# 3. Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 4. Run server
python main.py
```

Server runs at: **http://localhost:8000**

### Verify Installation

```bash
# Test setup
python test_setup.py

# Test data layer
python test_data.py

# Check API docs
# Open browser: http://localhost:8000/docs
```

## 📊 System Architecture

```
┌─────────────────┐
│  React Frontend │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ FastAPI  │
    │ Gateway  │
    └────┬─────┘
         │
    ┌────▼──────────────────────┐
    │   Core Services           │
    ├───────────────────────────┤
    │ • Prediction Service      │
    │ • Optimization Service    │
    │ • Explanation Service     │
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │   ML Models               │
    ├───────────────────────────┤
    │ • XGBoost Price Predictor │
    │ • RandomForest Demand     │
    │ • Spoilage Risk Model     │
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │   Data Layer              │
    ├───────────────────────────┤
    │ • AGMARKNET API           │
    │ • Weather API             │
    │ • SQLite Database         │
    │ • Static Data (JSON)      │
    └───────────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **ML/AI**: XGBoost, scikit-learn, pandas
- **Database**: SQLite (PostgreSQL for production)
- **APIs**: AGMARKNET, OpenWeather, LLM

### Frontend
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

### Deployment
- **Containerization**: Docker
- **Cloud**: AWS (Elastic Beanstalk, ECS, or Lambda)
- **CDN**: CloudFront for frontend

## 📁 Project Structure

```
rpin-prototype/
├── backend/                    # FastAPI backend
│   ├── main.py                # Application entry point
│   ├── app/
│   │   ├── core/              # ✅ Config, logging, exceptions
│   │   ├── models/            # ✅ Pydantic models
│   │   ├── data/              # ✅ Data access layer
│   │   ├── api/               # ⏭️ API endpoints
│   │   ├── services/          # ⏭️ Business logic
│   │   └── ml/                # ⏭️ ML models
│   └── data/                  # ✅ Static data files
│
├── frontend/                   # ⏭️ React frontend
│
├── .kiro/specs/               # Specification documents
│
└── docs/                      # Documentation
    ├── HOW_TO_RUN.md         # Quick reference guide
    ├── DEVELOPMENT_GUIDE.md  # Detailed development guide
    ├── QUICKSTART.md         # Hackathon quick start
    └── PROJECT_STRUCTURE.md  # Complete structure
```

## 🎨 Key Features

### 1. Intelligent Price Prediction
- 7-day price forecasts using XGBoost
- Historical mandi price analysis
- Confidence intervals

### 2. Demand Classification
- Low/Medium/High demand levels
- RandomForest classifier
- Market trend analysis

### 3. Spoilage Risk Assessment
- Weather-based risk calculation
- Crop-specific shelf life
- Transport duration impact

### 4. Profit Optimization
- Multi-market comparison
- Transport cost calculation
- Net profit maximization

### 5. Natural Language Explanations
- LLM-generated recommendations
- Simple language for rural users
- Key factor highlighting

## 📊 Sample Data

### Crops (6)
- Tomato, Onion, Potato, Cabbage, Carrot, Cauliflower

### Markets (6)
- Madurai, Chennai, Coimbatore, Trichy, Salem, Erode

### Villages (8)
- Theni, Dindigul, Salem, Erode, Namakkal, Karur, Tirupur, Pollachi

## 🧪 Testing

### Run Tests
```bash
# Setup verification
python test_setup.py

# Data layer test
python test_data.py

# API tests (once endpoints are implemented)
pytest
```

### Manual Testing
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **HOW_TO_RUN.md** | Quick reference for running the application |
| **DEVELOPMENT_GUIDE.md** | Detailed development guide with examples |
| **QUICKSTART.md** | Hackathon-specific rapid development guide |
| **PROJECT_STRUCTURE.md** | Complete project structure documentation |
| **architecture-diagram.md** | System architecture diagrams |

## 🔐 Configuration

Create `.env` file from `.env.example`:

```env
# External API Keys (optional for MVP)
OPENWEATHER_API_KEY=your_key_here
LLM_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./rpin.db

# Settings
FORECAST_DAYS=7
MIN_MARKETS_TO_ANALYZE=3
```

## 🚢 Deployment

### Local Development
```bash
python main.py
```

### Docker
```bash
docker build -t rpin-backend .
docker run -p 8000:8000 rpin-backend
```

### AWS Elastic Beanstalk
```bash
eb init -p python-3.9 rpin-backend
eb create rpin-env
eb deploy
```

## 📈 Development Roadmap

### Phase 1: Core Backend (Days 1-2) ✅
- [x] Project structure
- [x] Data models
- [x] Data integration layer

### Phase 2: ML & Logic (Days 2-3) ⏭️
- [ ] Price prediction model
- [ ] Demand classification
- [ ] Spoilage risk calculator
- [ ] Profit optimization

### Phase 3: API & Frontend (Days 3-4) ⏭️
- [ ] REST API endpoints
- [ ] React frontend
- [ ] Integration

### Phase 4: Deployment (Day 4) ⏭️
- [ ] AWS deployment
- [ ] Demo preparation
- [ ] Testing

## 🎯 MVP Features for Hackathon

Focus on:
1. ✅ Core infrastructure
2. ✅ Data models and validation
3. ⏭️ Simplified ML models (can use rule-based initially)
4. ⏭️ Main prediction endpoint
5. ⏭️ Basic React UI
6. ⏭️ Demo scenarios

## 🤝 Contributing

This is a hackathon project. For development:

1. Follow the task list in `.kiro/specs/rural-producer-intelligence-network/tasks.md`
2. Test changes using `http://localhost:8000/docs`
3. Check logs in `logs/` directory
4. Update documentation as needed

## 📝 License

This project is developed for a national hackathon under the theme "AI for Rural Innovation & Sustainable Systems".

## 🆘 Support

- Check **HOW_TO_RUN.md** for quick reference
- Check **DEVELOPMENT_GUIDE.md** for detailed guidance
- Review logs in `logs/` directory
- Test setup with `python test_setup.py`

## 🎉 Demo Scenario

**Example**: Tomato farmer in Theni with 1000 kg harvest

**Input**:
- Village: Theni
- Crop: Tomato
- Quantity: 1000 kg
- Harvest Date: 3 days from now

**Expected Output**:
```
Recommended Market: Madurai Mandi
Expected Profit: ₹20,800
Price: ₹28.50/kg
Transport Cost: ₹2,400
Spoilage Risk: 5.2%
Demand: High

Explanation: "For 1000 kg of tomatoes from Theni, selling in 
Madurai after 3 days gives ₹20,800 profit which is ₹7,300 more 
than the local market due to rising prices and lower spoilage risk."
```

## 🚀 Get Started Now!

```bash
cd backend
setup.bat  # or ./setup.sh on Linux/Mac
python main.py
```

Then open: **http://localhost:8000/docs**

Happy coding! 🎯
