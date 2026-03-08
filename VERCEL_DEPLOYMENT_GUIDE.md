# RPIN Deployment on Vercel (Without AWS)

## ✅ Yes, You Can Deploy on Vercel!

Vercel is an excellent alternative to AWS for deploying RPIN. It's simpler, faster, and perfect for hackathons!

---

## 🎯 Deployment Strategy

### Architecture on Vercel

```
Frontend (Vercel) → Backend (Vercel Serverless Functions) → External APIs
                                    ↓
                            Vercel Postgres (Database)
                                    ↓
                            Vercel KV (Redis Cache)
```

---

## 📦 Option 1: Full Stack on Vercel (Recommended)

### Step 1: Prepare Backend for Vercel

Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "OPENWEATHER_API_KEY": "@openweather-api-key",
    "LLM_API_KEY": "@llm-api-key"
  }
}
```

### Step 2: Update Backend for Serverless

Create `backend/vercel_app.py`:

```python
"""
Vercel-compatible FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.core.config import settings
from app.api.v1 import api_router
from app.data.database import init_database
from app.data.loaders import data_loader

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered market recommendation system for rural producers"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel will handle this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    try:
        init_database()
        data_loader.load_crops()
        data_loader.load_markets()
        data_loader.load_distances()
    except Exception as e:
        print(f"Startup error: {e}")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Welcome to RPIN - Rural Producer Intelligence Network",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

# Vercel handler
handler = Mangum(app)
```

### Step 3: Update requirements.txt

Add to `backend/requirements.txt`:

```txt
mangum==0.17.0
```

### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: rpin
# - Directory: ./
# - Override settings? No

# Set environment variables
vercel env add OPENWEATHER_API_KEY
vercel env add LLM_API_KEY

# Deploy to production
vercel --prod
```

**That's it!** Your app is now live at: `https://rpin.vercel.app`

---

## 📦 Option 2: Separate Frontend & Backend

### Frontend on Vercel

```bash
# Deploy frontend only
cd frontend
vercel

# Update API URL in index.html to your backend URL
```

### Backend on Railway/Render (Free Alternatives)

**Railway** (Recommended):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Deploy
railway up

# Add environment variables
railway variables set OPENWEATHER_API_KEY=xxx
railway variables set LLM_API_KEY=xxx
```

**Render** (Alternative):
1. Go to https://render.com
2. Connect GitHub repository
3. Create new Web Service
4. Select `backend` directory
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables
8. Deploy!

---

## 🗄️ Database Options (Without AWS)

### Option 1: Vercel Postgres (Recommended)

```bash
# Add Vercel Postgres to your project
vercel postgres create

# Get connection string
vercel env pull

# Update backend/app/core/config.py
DATABASE_URL = os.getenv("POSTGRES_URL")
```

**Pricing**: 
- Free tier: 256 MB storage, 60 hours compute/month
- Pro: $20/month for 512 MB

### Option 2: Supabase (Free PostgreSQL)

1. Go to https://supabase.com
2. Create new project
3. Get connection string from Settings → Database
4. Update `.env`:
```env
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

**Pricing**: Free tier with 500 MB database

### Option 3: PlanetScale (Free MySQL)

1. Go to https://planetscale.com
2. Create database
3. Get connection string
4. Update database driver to MySQL

**Pricing**: Free tier with 5 GB storage

### Option 4: SQLite (Simplest for Demo)

Keep using SQLite - works fine on Vercel for demos!

```python
# In backend/app/core/config.py
DATABASE_URL = "sqlite:///./rpin.db"
```

**Note**: Data resets on each deployment (serverless limitation)

---

## 🚀 Complete Vercel Deployment Steps

### Step 1: Prepare Project Structure

```
rpin-prototype/
├── vercel.json              # Vercel configuration
├── backend/
│   ├── vercel_app.py       # Vercel-compatible app
│   ├── requirements.txt    # Add mangum
│   └── ... (existing files)
└── frontend/
    └── index.html          # Update API URL
```

### Step 2: Create vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/vercel_app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/vercel_app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/index.html"
    }
  ]
}
```

### Step 3: Update Frontend API URL

In `frontend/index.html`, change:

```javascript
// From:
const API_BASE_URL = 'http://localhost:8000/api/v1';

// To:
const API_BASE_URL = 'https://rpin.vercel.app/api/v1';
// Or use relative URL:
const API_BASE_URL = '/api/v1';
```

### Step 4: Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (from project root)
vercel

# Set environment variables
vercel env add OPENWEATHER_API_KEY production
vercel env add LLM_API_KEY production

# Deploy to production
vercel --prod
```

### Step 5: Access Your App

- **Frontend**: https://rpin.vercel.app
- **API**: https://rpin.vercel.app/api/v1/predict
- **Docs**: https://rpin.vercel.app/docs

---

## 🎨 Alternative: Frontend on Vercel, Backend Elsewhere

### Frontend on Vercel

```bash
cd frontend
vercel
```

### Backend Options

**1. Render.com** (Free tier available)
```bash
# Create render.yaml
services:
  - type: web
    name: rpin-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: LLM_API_KEY
        sync: false
```

**2. Railway.app** (Free $5 credit/month)
```bash
railway init
railway up
```

**3. Fly.io** (Free tier available)
```bash
fly launch
fly deploy
```

**4. Heroku** (Free tier removed, but $7/month)
```bash
heroku create rpin-backend
git push heroku main
```

---

## 💰 Cost Comparison

### Vercel (Full Stack)
- **Hobby Plan**: FREE
  - 100 GB bandwidth
  - Serverless functions
  - Automatic HTTPS
  - Global CDN
- **Pro Plan**: $20/month
  - Unlimited bandwidth
  - Advanced analytics
  - Team collaboration

### Alternative Stack (All Free)
- **Frontend**: Vercel (Free)
- **Backend**: Railway (Free $5/month credit)
- **Database**: Supabase (Free 500 MB)
- **Total**: FREE! 🎉

### AWS Comparison
- **AWS**: ~$55-60/month
- **Vercel**: FREE (Hobby) or $20/month (Pro)
- **Savings**: $35-60/month or 100% free!

---

## 🔧 Vercel-Specific Optimizations

### 1. Edge Functions (Faster)

Create `backend/api/edge/predict.py`:

```python
from vercel_ai_sdk import Edge

@Edge
async def handler(request):
    # Ultra-fast edge function
    # Runs closer to users
    pass
```

### 2. Caching

Add to `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/api/v1/crops",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=3600, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### 3. Environment Variables

```bash
# Production
vercel env add OPENWEATHER_API_KEY production

# Development
vercel env add OPENWEATHER_API_KEY development

# Preview
vercel env add OPENWEATHER_API_KEY preview
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"

**Solution**: Ensure all dependencies in `requirements.txt`

```bash
pip freeze > requirements.txt
```

### Issue: "Function timeout"

**Solution**: Increase timeout in `vercel.json`

```json
{
  "functions": {
    "backend/vercel_app.py": {
      "maxDuration": 30
    }
  }
}
```

### Issue: "Database connection failed"

**Solution**: Use connection pooling

```python
from sqlalchemy.pool import NullPool

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool  # For serverless
)
```

### Issue: "CORS errors"

**Solution**: Update CORS in backend

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rpin.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Vercel vs AWS Comparison

| Feature | Vercel | AWS |
|---------|--------|-----|
| **Setup Time** | 5 minutes | 2-4 hours |
| **Cost (Free Tier)** | FREE forever | 12 months |
| **Cost (Paid)** | $20/month | $55-60/month |
| **Deployment** | `vercel` | Multiple steps |
| **HTTPS** | Automatic | Manual setup |
| **CDN** | Included | Extra cost |
| **Scaling** | Automatic | Manual config |
| **Database** | Add-on | Separate service |
| **Complexity** | Low | High |
| **Best For** | Hackathons, MVPs | Production, Enterprise |

---

## 🎯 Recommended Approach for Hackathon

### Quick & Free Stack

1. **Frontend**: Vercel (Free)
2. **Backend**: Railway (Free $5 credit)
3. **Database**: Supabase (Free)
4. **Total Cost**: $0
5. **Setup Time**: 30 minutes

### Commands

```bash
# Frontend
cd frontend
vercel

# Backend
cd backend
railway init
railway up
railway variables set OPENWEATHER_API_KEY=xxx

# Database
# Sign up at supabase.com
# Create project
# Copy connection string to Railway
```

**Done!** Your app is live and free! 🎉

---

## 📝 Complete Vercel Deployment Checklist

- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Create `vercel.json` in project root
- [ ] Add `mangum` to `requirements.txt`
- [ ] Create `backend/vercel_app.py`
- [ ] Update frontend API URL
- [ ] Login to Vercel: `vercel login`
- [ ] Deploy: `vercel`
- [ ] Add environment variables
- [ ] Deploy to production: `vercel --prod`
- [ ] Test all endpoints
- [ ] Update documentation with URLs

---

## 🎉 Success!

Your RPIN application is now deployed on Vercel!

**Advantages**:
- ✅ **Free**: No cost for hobby projects
- ✅ **Fast**: Global CDN, edge functions
- ✅ **Simple**: One command deployment
- ✅ **Automatic**: HTTPS, scaling, monitoring
- ✅ **Perfect for Hackathons**: Quick setup, reliable

**URLs**:
- Frontend: https://rpin.vercel.app
- API: https://rpin.vercel.app/api/v1
- Docs: https://rpin.vercel.app/docs

**Next Steps**:
1. Test all functionality
2. Share URL with judges
3. Monitor analytics
4. Iterate based on feedback

Good luck with your hackathon! 🚀
