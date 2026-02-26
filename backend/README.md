# RPIN Backend

Rural Producer Intelligence Network - FastAPI Backend

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
```

### 4. Run Development Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── app/
│   ├── __init__.py
│   ├── core/              # Core configuration and utilities
│   │   ├── config.py      # Settings management
│   │   ├── logging.py     # Logging configuration
│   │   └── exceptions.py  # Custom exceptions
│   ├── api/               # API endpoints
│   │   └── v1/            # API version 1
│   ├── models/            # Pydantic models (coming in Task 2)
│   ├── services/          # Business logic (coming in Task 5-7)
│   ├── ml/                # ML models (coming in Task 5)
│   └── data/              # Data access layer (coming in Task 3)
├── data/                  # Static data files
│   ├── crops.json
│   ├── markets.json
│   └── distances.json
├── models/                # Trained ML models
└── logs/                  # Application logs
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Next Steps

- Task 2: Implement data models and validation
- Task 3: Implement external data integration
- Task 5: Implement ML prediction models
