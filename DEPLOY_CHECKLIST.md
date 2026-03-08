# RPIN Deployment Checklist

## Pre-Deployment Checklist

### ✅ Files Ready for Deployment

- [x] `vercel.json` - Vercel configuration
- [x] `requirements.txt` - Python dependencies
- [x] `package.json` - NPM configuration
- [x] `.vercelignore` - Exclude unnecessary files
- [x] `api/index.py` - Serverless entry point
- [x] `backend/` - Complete backend code
- [x] `frontend/index.html` - Web interface
- [x] `backend/data/` - Sample data files

### ✅ Configuration Verified

- [x] Frontend API URL auto-detection configured
- [x] CORS settings allow Vercel domains
- [x] All imports use relative paths
- [x] No hardcoded localhost URLs (except for local dev)

### ✅ Data Files Present

- [x] `backend/data/crops.json` (6 crops)
- [x] `backend/data/markets.json` (6 markets)
- [x] `backend/data/distances.json` (8 villages)

## Deployment Steps

### Option A: GitHub + Vercel Dashboard (Recommended)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - RPIN application"
   ```

2. **Push to GitHub**
   - Create new repo on GitHub: https://github.com/new
   - Name it: `rpin` or `rural-producer-intelligence-network`
   - Run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Vercel**
   - Go to: https://vercel.com/new
   - Click "Import Git Repository"
   - Select your GitHub repo
   - Click "Deploy"
   - Wait 2-3 minutes
   - Done! ✅

### Option B: Vercel CLI (Alternative)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

## Post-Deployment Testing

### 1. Test Health Endpoint
```bash
curl https://your-app.vercel.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "RPIN - Rural Producer Intelligence Network",
  "version": "1.0.0"
}
```

### 2. Test API Documentation
Visit: `https://your-app.vercel.app/docs`

Should show interactive Swagger UI.

### 3. Test Frontend
Visit: `https://your-app.vercel.app/`

Should show the RPIN web interface.

### 4. Test Prediction API
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

Expected: JSON response with market recommendations.

### 5. Test All Endpoints

- ✅ `GET /` - Frontend
- ✅ `GET /health` - Health check
- ✅ `GET /docs` - API documentation
- ✅ `POST /api/v1/predict` - Market prediction
- ✅ `GET /api/v1/markets` - List markets
- ✅ `GET /api/v1/crops` - List crops

## Common Issues & Fixes

### Issue 1: "Module not found"
**Fix:** Check that `api/index.py` correctly adds backend to Python path.

### Issue 2: "Function timeout"
**Fix:** Increase timeout in `vercel.json`:
```json
"functions": {
  "api/index.py": {
    "maxDuration": 60
  }
}
```

### Issue 3: CORS errors
**Fix:** Add your Vercel URL to `backend/app/core/config.py`:
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://your-app.vercel.app",
    "https://*.vercel.app"
]
```

### Issue 4: Data files not found
**Fix:** Ensure `backend/data/*.json` files are not in `.vercelignore`.

## Deployment URL

After deployment, your app will be available at:
- **Production:** `https://your-project-name.vercel.app`
- **Preview:** `https://your-project-name-git-branch.vercel.app`

## Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Vercel handles HTTPS automatically

## Monitoring

View logs in real-time:
```bash
vercel logs --follow
```

Or check Vercel Dashboard:
- Function invocations
- Error rates
- Response times
- Bandwidth usage

## Demo Preparation

### For Hackathon Judges:

1. **Live Demo URL:** `https://your-app.vercel.app`
2. **API Docs:** `https://your-app.vercel.app/docs`
3. **GitHub Repo:** `https://github.com/YOUR_USERNAME/rpin`
4. **Demo Video:** Record screen showing:
   - Input form with sample data
   - Prediction results
   - Market comparison table
   - AI-generated explanation

### Sample Demo Data:

**Scenario 1: High Profit**
- Village: Theni
- Crop: Tomato
- Quantity: 1000 kg
- Harvest Date: (today + 3 days)

**Scenario 2: Spoilage Risk**
- Village: Dindigul
- Crop: Cabbage
- Quantity: 500 kg
- Harvest Date: (today + 7 days)

**Scenario 3: Transport Cost Impact**
- Village: Pollachi
- Crop: Potato
- Quantity: 2000 kg
- Harvest Date: (today + 2 days)

## Success Criteria

✅ Application deployed and accessible
✅ All API endpoints working
✅ Frontend loads and displays correctly
✅ Predictions return valid results
✅ No CORS errors
✅ Response time < 5 seconds
✅ API documentation accessible
✅ Mobile responsive design works

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Share demo URL with judges
4. ✅ Prepare presentation
5. ✅ Record demo video
6. ✅ Submit to hackathon

---

**Ready to deploy?** Follow Option A or B above! 🚀
