# Vercel Deployment Guide for RPIN

## Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - RPIN application"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/rpin.git
   git push -u origin main
   ```

2. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`
   - Click "Deploy"
   - Done! Your app will be live in 2-3 minutes

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Follow the prompts:**
   - Set up and deploy? Yes
   - Which scope? (Select your account)
   - Link to existing project? No
   - Project name? rpin (or your choice)
   - Directory? ./ (current directory)
   - Override settings? No

5. **Done!** Your deployment URL will be displayed.

## What's Included

This deployment package includes:

✅ **Backend API** (FastAPI)
- All ML models (price prediction, demand classification, spoilage prediction)
- Optimization engine
- REST API endpoints
- CORS configured for frontend

✅ **Frontend** (HTML/CSS/JavaScript)
- Responsive web interface
- Auto-detects API endpoint (localhost vs production)
- Form validation
- Results visualization

✅ **Data**
- 6 crops (tomato, onion, potato, cabbage, carrot, cauliflower)
- 6 markets (Madurai, Chennai, Coimbatore, Trichy, Salem, Erode)
- 8 villages with distance data
- Sample historical price data

✅ **Configuration**
- `vercel.json` - Vercel deployment configuration
- `requirements.txt` - Python dependencies
- `.vercelignore` - Files to exclude from deployment
- `package.json` - NPM scripts for easy deployment

## Project Structure for Vercel

```
rpin/
├── api/
│   └── index.py              # Vercel serverless entry point
├── backend/
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── data/             # Data loaders
│   │   ├── ml/               # ML models
│   │   ├── models/           # Pydantic models
│   │   └── services/         # Business logic
│   ├── data/                 # Static data files
│   │   ├── crops.json
│   │   ├── markets.json
│   │   └── distances.json
│   └── main.py               # FastAPI app
├── frontend/
│   └── index.html            # Web interface
├── vercel.json               # Vercel configuration
├── requirements.txt          # Python dependencies
└── package.json              # NPM configuration
```

## Environment Variables (Optional)

If you want to use external APIs, add these in Vercel Dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - `OPENWEATHER_API_KEY` - For weather data (optional)
   - `LLM_API_KEY` - For advanced explanations (optional)

## Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check**
   ```
   https://your-app.vercel.app/health
   ```

2. **API Documentation**
   ```
   https://your-app.vercel.app/docs
   ```

3. **Frontend**
   ```
   https://your-app.vercel.app/
   ```

4. **Test Prediction**
   ```bash
   curl -X POST https://your-app.vercel.app/api/v1/predict \
     -H "Content-Type: application/json" \
     -d '{
       "village_location": "Theni",
       "crop_type": "tomato",
       "quantity_kg": 1000,
       "harvest_date": "2024-03-15"
     }'
   ```

## Troubleshooting

### Issue: "Module not found" error

**Solution:** Make sure all imports in `backend/` use relative imports:
```python
from app.models.request import PredictionRequest  # ✅ Correct
from backend.app.models.request import PredictionRequest  # ❌ Wrong
```

### Issue: "Function timeout"

**Solution:** Increase timeout in `vercel.json`:
```json
"functions": {
  "api/index.py": {
    "maxDuration": 60
  }
}
```

### Issue: Frontend can't connect to API

**Solution:** Check browser console. The frontend auto-detects the API URL:
- Local: `http://localhost:8000/api/v1`
- Production: `/api/v1` (relative URL)

### Issue: CORS errors

**Solution:** Update `backend/app/core/config.py`:
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add your Vercel URL
    "*"  # Or allow all (not recommended for production)
]
```

## Cost

**Vercel Free Tier includes:**
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Serverless function executions
- ✅ Automatic HTTPS
- ✅ Custom domains

**Perfect for hackathons and demos!**

## Custom Domain (Optional)

1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. Done! Vercel handles HTTPS automatically

## Monitoring

View your deployment logs:
```bash
vercel logs
```

Or check the Vercel Dashboard for:
- Real-time logs
- Function invocations
- Bandwidth usage
- Error tracking

## Updating Your Deployment

After making changes:

```bash
git add .
git commit -m "Update description"
git push
```

Vercel will automatically redeploy! 🚀

## Support

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Project Issues: Create an issue in your GitHub repo

---

**Ready to deploy?** Run `vercel --prod` or push to GitHub and import to Vercel!
