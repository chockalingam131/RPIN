# RPIN Prototype Quick Start Guide

## 🎯 Hackathon Prototype Strategy

This guide helps you build a working RPIN prototype quickly for your hackathon demo.

## 📋 Prerequisites

- Python 3.9+ installed
- Node.js 16+ and npm installed
- Git installed
- AWS account (optional for deployment)
- OpenWeather API key (free tier)
- OpenAI API key or similar LLM API (for explanations)

## 🚀 Phase 1: Local Development (Days 1-3)

### Step 1: Project Setup (30 minutes)

```bash
# Create project directory
mkdir rpin-prototype
cd rpin-prototype

# Create backend directory
mkdir backend
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic pandas scikit-learn xgboost python-multipart requests python-dotenv
```

### Step 2: Create Synthetic Data (1 hour)

Create sample data files to avoid external API dependencies initially:

**backend/data/crops.json**
```json
{
  "tomato": {"shelf_life_days": 7, "optimal_temp": 15, "humidity_tolerance": 85},
  "onion": {"shelf_life_days": 30, "optimal_temp": 25, "humidity_tolerance": 70},
  "potato": {"shelf_life_days": 45, "optimal_temp": 10, "humidity_tolerance": 90},
  "cabbage": {"shelf_life_days": 14, "optimal_temp": 5, "humidity_tolerance": 95}
}
```

**backend/data/markets.json**
```json
{
  "madurai": {"name": "Madurai Mandi", "location": "Madurai", "capacity_tons": 500},
  "chennai": {"name": "Koyambedu Market", "location": "Chennai", "capacity_tons": 1000},
  "coimbatore": {"name": "Coimbatore Market", "location": "Coimbatore", "capacity_tons": 300},
  "trichy": {"name": "Trichy Mandi", "location": "Trichy", "capacity_tons": 400}
}
```

**backend/data/distances.json** (village to market distances in km)
```json
{
  "theni": {"madurai": 80, "chennai": 520, "coimbatore": 180, "trichy": 200},
  "dindigul": {"madurai": 65, "chennai": 450, "coimbatore": 120, "trichy": 140},
  "salem": {"madurai": 250, "chennai": 340, "coimbatore": 120, "trichy": 180}
}
```

### Step 3: Implement Core Backend (Day 1-2)

Follow the tasks in `.kiro/specs/rural-producer-intelligence-network/tasks.md`:

**Priority Tasks for MVP:**
1. ✅ Task 1: Set up project structure
2. ✅ Task 2.1: Create data models
3. ✅ Task 2.3: Database setup (use simple JSON files initially)
4. ⚠️ Task 3: Skip external APIs, use mock data
5. ✅ Task 5.1: Price prediction (use simple linear model initially)
6. ✅ Task 5.3: Demand classification (rule-based initially)
7. ✅ Task 5.4: Spoilage risk predictor
8. ✅ Task 6.1: Transport cost calculator
9. ✅ Task 6.3: Profit optimization
10. ✅ Task 7.1: LLM explanations (use templates initially)
11. ✅ Task 9: FastAPI endpoints
12. ✅ Task 10: React frontend

### Step 4: Simplified ML Models (Day 2)

For the prototype, use simplified models:

**Price Prediction**: Use historical average + random variation
```python
def predict_price(crop, market, days=7):
    base_prices = {"tomato": 25, "onion": 30, "potato": 20, "cabbage": 15}
    base = base_prices.get(crop, 20)
    return [base + random.uniform(-5, 10) for _ in range(days)]
```

**Demand Classification**: Rule-based on price trends
```python
def classify_demand(prices):
    trend = prices[-1] - prices[0]
    if trend > 5: return "High"
    elif trend < -5: return "Low"
    return "Medium"
```

**Spoilage Risk**: Simple formula
```python
def calculate_spoilage(crop_shelf_life, transport_days, temperature):
    risk = (transport_days / crop_shelf_life) * 100
    if temperature > 30: risk *= 1.5
    return min(risk, 100)
```

### Step 5: Frontend Setup (Day 3)

```bash
# In project root
npx create-react-app frontend
cd frontend
npm install axios tailwindcss
```

Create a simple form and results display following Task 10 in tasks.md.

## 🌐 Phase 2: AWS Deployment (Day 4)

### Option A: Simple AWS Deployment (Recommended for Hackathon)

**AWS Elastic Beanstalk** (Easiest)
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
eb init -p python-3.9 rpin-backend

# Create environment and deploy
eb create rpin-env
eb deploy
```

**Frontend on S3 + CloudFront**
```bash
# Build frontend
cd frontend
npm run build

# Deploy to S3
aws s3 sync build/ s3://rpin-frontend-bucket
```

### Option B: Docker + AWS ECS (More Professional)

**Create Dockerfile for backend:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy to ECS:**
- Push Docker image to ECR
- Create ECS task definition
- Deploy to Fargate

### Option C: AWS Lambda + API Gateway (Serverless)

For lightweight demo:
- Backend: Lambda functions + API Gateway
- Frontend: S3 + CloudFront
- Data: DynamoDB or S3

## 🎨 Demo Data Preparation

Create realistic demo scenarios:

**Scenario 1: Tomato Farmer in Theni**
- Input: 1000 kg tomatoes, harvest in 3 days
- Expected: Madurai market recommended (closer, good price)

**Scenario 2: Onion Farmer in Dindigul**
- Input: 2000 kg onions, harvest in 7 days
- Expected: Chennai market (higher price, low spoilage risk)

**Scenario 3: Potato Farmer in Salem**
- Input: 5000 kg potatoes, harvest tomorrow
- Expected: Coimbatore market (closest, urgent harvest)

## 📊 AWS Services Recommendation for Prototype

### Minimal Setup (Free Tier Eligible)
- **Compute**: EC2 t2.micro or Elastic Beanstalk
- **Storage**: S3 for static files
- **Database**: RDS Free Tier (PostgreSQL) or DynamoDB
- **API**: API Gateway (if using Lambda)
- **CDN**: CloudFront for frontend

### Cost Estimate
- **Development/Demo**: $0-10/month (mostly free tier)
- **Hackathon Demo Day**: ~$5 for the day

## 🔧 Environment Variables

Create `.env` file:
```
OPENWEATHER_API_KEY=your_key_here
LLM_API_KEY=your_key_here
AWS_REGION=ap-south-1
DATABASE_URL=sqlite:///./rpin.db
```

## 📝 Development Checklist

### Day 1: Backend Core
- [ ] Project structure setup
- [ ] Data models created
- [ ] Mock data files ready
- [ ] Basic API endpoints working
- [ ] Test with Postman/curl

### Day 2: ML & Logic
- [ ] Price prediction working
- [ ] Demand classification working
- [ ] Spoilage calculation working
- [ ] Transport cost calculator working
- [ ] Profit optimization working
- [ ] Test end-to-end prediction

### Day 3: Frontend
- [ ] React app setup
- [ ] Input form created
- [ ] Results table display
- [ ] API integration working
- [ ] Basic styling complete

### Day 4: Deployment & Polish
- [ ] Backend deployed to AWS
- [ ] Frontend deployed to AWS
- [ ] Demo scenarios tested
- [ ] Presentation prepared
- [ ] Video demo recorded

## 🎯 Hackathon Demo Tips

1. **Prepare 3 demo scenarios** with different outcomes
2. **Have backup data** in case APIs fail
3. **Record a video demo** as backup
4. **Prepare slides** explaining the problem and solution
5. **Highlight AI/ML components** clearly
6. **Show social impact** - how it helps farmers
7. **Mention scalability** - how it can grow

## 🚨 Troubleshooting

**If ML models are slow:**
- Use pre-computed predictions
- Cache results aggressively

**If external APIs fail:**
- Always have fallback mock data
- Show cached results

**If deployment fails:**
- Have local demo ready
- Use ngrok to expose local server

## 📚 Next Steps

1. Start with Task 1 in `tasks.md`
2. Build incrementally, test frequently
3. Deploy early, deploy often
4. Focus on demo-ready features first
5. Polish UI last

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- AWS Elastic Beanstalk: https://docs.aws.amazon.com/elasticbeanstalk/
- XGBoost: https://xgboost.readthedocs.io/

Good luck with your hackathon! 🚀
