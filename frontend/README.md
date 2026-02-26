# RPIN Frontend

Simple HTML/JavaScript frontend for the Rural Producer Intelligence Network.

## Running the Frontend

### Option 1: Using Python HTTP Server

```bash
cd frontend
python -m http.server 3000
```

Then open: http://localhost:3000

### Option 2: Using Node.js HTTP Server

```bash
cd frontend
npx http-server -p 3000
```

Then open: http://localhost:3000

### Option 3: Open Directly

Simply open `index.html` in your browser.

**Note**: If you open directly, you may need to enable CORS in your browser or run the backend with CORS enabled (already configured).

## Configuration

The frontend is configured to connect to the backend at:
```
http://localhost:8000/api/v1
```

If your backend is running on a different port or host, edit the `API_BASE_URL` in `index.html`.

## Features

- ✅ Input form for producer details
- ✅ Village and crop selection
- ✅ Quantity and harvest date input
- ✅ Loading state with spinner
- ✅ Best market recommendation display
- ✅ Natural language explanation
- ✅ Comparison table for all markets
- ✅ Responsive design for mobile
- ✅ Error handling

## Usage

1. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```

2. Start the frontend server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

3. Open http://localhost:3000 in your browser

4. Fill in the form:
   - Select your village
   - Select your crop
   - Enter quantity in kg
   - Select harvest date

5. Click "Get Recommendations"

6. View results:
   - Best market recommendation
   - Expected profit
   - Explanation
   - Comparison table

## Supported Data

**Villages**: Theni, Dindigul, Salem, Erode, Namakkal, Karur, Tirupur, Pollachi

**Crops**: Tomato, Onion, Potato, Cabbage, Carrot, Cauliflower

**Markets**: Madurai, Chennai, Coimbatore, Trichy, Salem, Erode
