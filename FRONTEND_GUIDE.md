# 🎨 Frontend Deployment Guide

## Current Status

✅ **API is working!** You saw "API is running successfully!" - that's great!

The page you're seeing is a simple HTML interface. You also have a more complete frontend with a form interface.

## Option 1: Use the Complete Frontend (Recommended)

Your complete frontend is in `frontend/index.html` with a full form interface. Here's how to access it:

### Deploy Frontend to Vercel

1. **Open `frontend/index.html` in your browser locally:**
   ```bash
   # Windows
   start frontend/index.html
   
   # Or just double-click frontend/index.html
   ```

2. **Update the API URL in the file:**
   - Open `frontend/index.html`
   - Find line ~330: `const API_BASE_URL = ...`
   - Change it to your Vercel URL:
   ```javascript
   const API_BASE_URL = 'https://your-app.vercel.app';
   ```

3. **Deploy frontend separately:**
   - Create a new Vercel project for frontend
   - Or use GitHub Pages (free)
   - Or use Netlify (free)

### Quick Test Locally

1. **Open `frontend/index.html` in browser**
2. **Update API URL to your Vercel URL**
3. **Test the form:**
   - Village: Theni
   - Crop: Tomato
   - Quantity: 1000 kg
   - Date: (future date)
   - Click "Get Recommendations"

## Option 2: Test API Directly

You can test the API without the frontend using these methods:

### Method 1: Using curl

```bash
curl -X POST https://your-app.vercel.app/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "village_location": "theni",
    "crop_type": "tomato",
    "quantity_kg": 1000,
    "harvest_date": "2024-03-15"
  }'
```

### Method 2: Using Browser Console

1. Open your Vercel app: `https://your-app.vercel.app/`
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Paste this code:

```javascript
fetch('https://your-app.vercel.app/api/v1/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    village_location: 'theni',
    crop_type: 'tomato',
    quantity_kg: 1000,
    harvest_date: '2024-03-15'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Method 3: Using Postman/Insomnia

1. Open Postman or Insomnia
2. Create new POST request
3. URL: `https://your-app.vercel.app/api/v1/predict`
4. Headers: `Content-Type: application/json`
5. Body (JSON):
```json
{
  "village_location": "theni",
  "crop_type": "tomato",
  "quantity_kg": 1000,
  "harvest_date": "2024-03-15"
}
```
6. Send!

## Option 3: Create Simple Test Page

Create a file `test.html` with this content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>RPIN Test</title>
    <style>
        body { font-family: Arial; padding: 20px; max-width: 800px; margin: 0 auto; }
        button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>🌾 RPIN Test</h1>
    <button onclick="testAPI()">Test Prediction API</button>
    <div id="result"></div>
    
    <script>
        async function testAPI() {
            const result = document.getElementById('result');
            result.innerHTML = '<p>Loading...</p>';
            
            try {
                const response = await fetch('https://your-app.vercel.app/api/v1/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        village_location: 'theni',
                        crop_type: 'tomato',
                        quantity_kg: 1000,
                        harvest_date: '2024-03-15'
                    })
                });
                
                const data = await response.json();
                result.innerHTML = '<h2>✅ Success!</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                result.innerHTML = '<h2>❌ Error</h2><p>' + error.message + '</p>';
            }
        }
    </script>
</body>
</html>
```

Replace `your-app.vercel.app` with your actual Vercel URL, then open this file in your browser.

## What You Should See

When you test the API, you should get a response like:

```json
{
  "request_id": "req_20240315_123456",
  "village_location": "theni",
  "crop_type": "tomato",
  "quantity_kg": 1000,
  "markets": [
    {
      "market_id": "madurai",
      "market_name": "Madurai Mandi",
      "predicted_price": 28.50,
      "demand_level": "High",
      "spoilage_risk_percent": 12.3,
      "distance_km": 80,
      "transport_cost": 3200.00,
      "net_profit": 25300.00
    },
    ...more markets...
  ],
  "best_market": "Madurai Mandi",
  "explanation": "For 1000kg of Tomato from Theni, selling in Madurai Mandi gives ₹25,300 profit..."
}
```

## Available Endpoints

Test these in your browser:

1. **Root:** `https://your-app.vercel.app/`
   - Shows API status page

2. **Health Check:** `https://your-app.vercel.app/health`
   - Returns: `{"status": "healthy", ...}`

3. **List Crops:** `https://your-app.vercel.app/api/v1/crops`
   - Returns list of 6 crops

4. **List Markets:** `https://your-app.vercel.app/api/v1/markets`
   - Returns list of 6 markets

5. **Predict (POST):** `https://your-app.vercel.app/api/v1/predict`
   - Requires JSON body with village, crop, quantity, date

## Supported Data

**Villages:** theni, dindigul, salem, erode, namakkal, karur, tirupur, pollachi

**Crops:** tomato, onion, potato, cabbage, carrot, cauliflower

**Markets:** Madurai, Chennai, Coimbatore, Trichy, Salem, Erode

## Next Steps

1. ✅ API is working (you confirmed this!)
2. ✅ Test predictions using one of the methods above
3. ✅ Deploy frontend separately (optional)
4. ✅ Record demo video showing predictions
5. ✅ Submit to hackathon

## Demo Video Tips

Record your screen showing:
1. Open your Vercel app
2. Show the API status page
3. Test a prediction (using curl, Postman, or test page)
4. Show the JSON response with market recommendations
5. Explain the features (price prediction, demand, spoilage risk, profit)

Keep it under 3 minutes!

## Congratulations! 🎉

Your API is deployed and working on Vercel! You can now:
- Make predictions
- Get market recommendations
- Calculate profits
- All features are working!

**Your app is live and ready for the hackathon!** 🚀
