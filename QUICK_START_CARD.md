# RPIN Quick Start Card

## 🚀 Run in 3 Steps

### Step 1: Start Backend
```bash
cd backend
venv\Scripts\activate  # Windows: venv\Scripts\activate
python main.py
```
✅ Backend: http://localhost:8000
📚 API Docs: http://localhost:8000/docs

### Step 2: Start Frontend
```bash
cd frontend
python -m http.server 3000
```
✅ Frontend: http://localhost:3000

### Step 3: Use Application
1. Open: http://localhost:3000
2. Select: Village, Crop, Quantity, Date
3. Click: "Get Recommendations"
4. View: Best market, profit, explanation

---

## 📊 Demo Scenarios

### Scenario 1: Tomato from Theni
- Village: Theni
- Crop: Tomato
- Quantity: 1000 kg
- Date: 3 days from now
- **Result**: Madurai Mandi, ₹20,800 profit

### Scenario 2: Onion from Dindigul
- Village: Dindigul
- Crop: Onion
- Quantity: 2000 kg
- Date: 7 days from now
- **Result**: Chennai, ₹45,600 profit

### Scenario 3: Potato from Salem
- Village: Salem
- Crop: Potato
- Quantity: 5000 kg
- Date: Tomorrow
- **Result**: Salem (local), ₹82,500 profit

---

## 🌐 AWS Deployment (Quick)

```bash
# Install tools
pip install awsebcli

# Deploy backend
cd backend
eb init -p python-3.9 rpin-backend
eb create rpin-env
eb setenv OPENWEATHER_API_KEY=xxx

# Deploy frontend
cd frontend
aws s3 mb s3://rpin-frontend-unique
aws s3 sync . s3://rpin-frontend-unique --acl public-read
```

---

## 🔧 Troubleshooting

**Backend won't start?**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend won't load?**
```bash
cd frontend
python -m http.server 3000
# Or open index.html directly
```

**API not working?**
- Check: http://localhost:8000/health
- Verify: Backend is running
- Check: Browser console (F12)

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **COMPLETE_GUIDE.md** | Everything in one place |
| **USER_GUIDE.md** | How to use the application |
| **AWS_DEPLOYMENT_GUIDE.md** | Deploy to AWS |
| **README.md** | Project overview |

---

## 🎯 Key Features

✅ AI-powered price predictions
✅ Demand classification (High/Medium/Low)
✅ Spoilage risk assessment
✅ Transport cost optimization
✅ Profit maximization
✅ Natural language explanations
✅ Multi-market comparison
✅ Responsive web interface

---

## 📞 Quick Help

**Health Check**: http://localhost:8000/health
**API Docs**: http://localhost:8000/docs
**Logs**: backend/logs/rpin_*.log
**Test**: python test_setup.py

---

## 🎉 Success Indicators

✅ Backend shows: "Uvicorn running on http://0.0.0.0:8000"
✅ Frontend shows: "Serving HTTP on 0.0.0.0 port 3000"
✅ Health check returns: {"status": "healthy"}
✅ Form submission shows results

---

## 💡 Pro Tips

1. **Keep terminals open** during demo
2. **Test before presenting** with all 3 scenarios
3. **Have screenshots ready** as backup
4. **Explain AI components** (XGBoost, RandomForest)
5. **Highlight social impact** (helping farmers)

---

## 🏆 Hackathon Pitch

**Problem**: Farmers lose money due to poor market decisions

**Solution**: AI-powered recommendations for:
- Best market to sell
- Optimal timing
- Expected profit
- Risk assessment

**Impact**:
- 📈 Maximize farmer profits
- 🎯 Reduce food wastage
- 📊 Data-driven decisions
- 🌾 Support rural communities

**Tech**: FastAPI + ML Models + AWS

**Scalable**: Can expand to all crops, markets, regions

---

## ✅ Pre-Demo Checklist

- [ ] Backend running
- [ ] Frontend accessible
- [ ] Tested 3 scenarios
- [ ] Screenshots ready
- [ ] Presentation prepared
- [ ] Internet working
- [ ] Backup plan ready

---

## 🚀 You're Ready!

**Local**: http://localhost:3000
**API**: http://localhost:8000/docs
**Guide**: COMPLETE_GUIDE.md

Good luck! 🎯
