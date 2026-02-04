# RPIN System Architecture Diagrams

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React Web Interface]
        Forms[Input Forms]
        Results[Results Display]
    end
    
    subgraph "API Gateway Layer"
        Gateway[FastAPI Gateway]
        Auth[Authentication]
        Rate[Rate Limiting]
    end
    
    subgraph "Core Services"
        PredictionService[Prediction Service]
        OptimizationService[Optimization Service]
        ExplanationService[Explanation Service]
    end
    
    subgraph "ML Models"
        PriceModel[XGBoost Price Predictor]
        DemandModel[RandomForest Demand Classifier]
        SpoilageModel[Spoilage Risk Predictor]
    end
    
    subgraph "Data Layer"
        MandiData[Mandi Price Database]
        WeatherAPI[Weather API Client]
        CropDB[Crop Shelf-life Database]
        DistanceDB[Village-Market Distance DB]
    end
    
    subgraph "External APIs"
        AGMARKNET[AGMARKNET API]
        OpenWeather[OpenWeather API]
        LLM[LLM API for Explanations]
    end
    
    UI --> Gateway
    Forms --> Gateway
    Results --> Gateway
    
    Gateway --> PredictionService
    Gateway --> OptimizationService
    Gateway --> ExplanationService
    
    PredictionService --> PriceModel
    PredictionService --> DemandModel
    PredictionService --> SpoilageModel
    
    PredictionService --> MandiData
    PredictionService --> WeatherAPI
    PredictionService --> CropDB
    
    OptimizationService --> DistanceDB
    
    MandiData --> AGMARKNET
    WeatherAPI --> OpenWeather
    ExplanationService --> LLM
```

## Data Flow Architecture

```mermaid
flowchart TD
    A[Producer Input] --> B{Input Validation}
    B -->|Valid| C[Data Collection Phase]
    B -->|Invalid| D[Error Response]
    
    C --> E[Fetch Weather Data]
    C --> F[Fetch Historical Prices]
    C --> G[Load Crop Info]
    C --> H[Load Distance Data]
    
    E --> I[ML Prediction Phase]
    F --> I
    G --> I
    H --> I
    
    I --> J[Price Prediction - XGBoost]
    I --> K[Demand Classification - RandomForest]
    I --> L[Spoilage Risk Calculation]
    
    J --> M[Optimization Phase]
    K --> M
    L --> M
    H --> M
    
    M --> N[Transport Cost Calculation]
    M --> O[Net Profit Calculation]
    M --> P[Market Ranking]
    
    N --> Q[Results Generation]
    O --> Q
    P --> Q
    
    Q --> R[LLM Explanation Generation]
    Q --> S[Response Formatting]
    
    R --> T[Final Response]
    S --> T
    
    T --> U[Frontend Display]
```

## Component Interaction Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API_Gateway
    participant PredictionService
    participant OptimizationService
    participant ExplanationService
    participant External_APIs
    participant ML_Models
    
    User->>Frontend: Enter producer details
    Frontend->>API_Gateway: POST /api/v1/predict
    
    API_Gateway->>PredictionService: Process prediction request
    
    PredictionService->>External_APIs: Fetch weather data
    External_APIs-->>PredictionService: Weather forecast
    
    PredictionService->>External_APIs: Fetch mandi prices
    External_APIs-->>PredictionService: Historical price data
    
    PredictionService->>ML_Models: Price prediction
    ML_Models-->>PredictionService: 7-day price forecast
    
    PredictionService->>ML_Models: Demand classification
    ML_Models-->>PredictionService: Demand levels
    
    PredictionService->>ML_Models: Spoilage risk
    ML_Models-->>PredictionService: Spoilage percentages
    
    PredictionService-->>OptimizationService: Prediction results
    
    OptimizationService->>OptimizationService: Calculate transport costs
    OptimizationService->>OptimizationService: Compute net profits
    OptimizationService->>OptimizationService: Rank markets
    
    OptimizationService-->>ExplanationService: Optimization results
    
    ExplanationService->>External_APIs: Generate explanation
    External_APIs-->>ExplanationService: Natural language explanation
    
    ExplanationService-->>API_Gateway: Complete response
    API_Gateway-->>Frontend: Market recommendations
    Frontend-->>User: Display results table
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Frontend Container"
            ReactApp[React Application]
            Nginx[Nginx Web Server]
        end
        
        subgraph "Backend Container"
            FastAPI[FastAPI Application]
            Models[ML Models Cache]
            SQLite[SQLite Database]
        end
        
        subgraph "Data Storage"
            StaticFiles[JSON Config Files]
            ModelFiles[Pickle Model Files]
            Cache[Redis Cache - Optional]
        end
    end
    
    subgraph "External Services"
        AGMARKNET_API[AGMARKNET API]
        Weather_API[OpenWeather API]
        LLM_API[LLM API Service]
    end
    
    ReactApp --> Nginx
    Nginx --> FastAPI
    FastAPI --> Models
    FastAPI --> SQLite
    FastAPI --> StaticFiles
    FastAPI --> ModelFiles
    FastAPI --> Cache
    
    FastAPI --> AGMARKNET_API
    FastAPI --> Weather_API
    FastAPI --> LLM_API
    
    subgraph "Load Balancer - Optional"
        LB[Load Balancer]
    end
    
    LB --> Nginx
```

## Technology Stack Diagram

```mermaid
graph TB
    subgraph "Frontend Technologies"
        React[React 18+]
        TypeScript[TypeScript]
        TailwindCSS[Tailwind CSS]
        Axios[Axios HTTP Client]
    end
    
    subgraph "Backend Technologies"
        FastAPI[FastAPI Framework]
        Python[Python 3.9+]
        Pydantic[Pydantic Models]
        Uvicorn[Uvicorn ASGI Server]
    end
    
    subgraph "ML/AI Technologies"
        XGBoost[XGBoost Regressor]
        ScikitLearn[Scikit-learn]
        Pandas[Pandas DataFrames]
        Numpy[NumPy Arrays]
        Pickle[Model Serialization]
    end
    
    subgraph "Data Technologies"
        SQLite[SQLite Database]
        JSON[JSON Config Files]
        CSV[CSV Data Files]
    end
    
    subgraph "External APIs"
        AGMARKNET[AGMARKNET API]
        OpenWeather[OpenWeather API]
        OpenAI[OpenAI/LLM API]
    end
    
    subgraph "DevOps Technologies"
        Docker[Docker Containers]
        DockerCompose[Docker Compose]
        Git[Git Version Control]
    end
    
    React --> FastAPI
    FastAPI --> XGBoost
    FastAPI --> SQLite
    FastAPI --> AGMARKNET
    FastAPI --> OpenWeather
    FastAPI --> OpenAI
    
    Docker --> React
    Docker --> FastAPI
```

## Security and Performance Architecture

```mermaid
graph TB
    subgraph "Security Layer"
        CORS[CORS Configuration]
        RateLimit[Rate Limiting]
        InputValidation[Input Validation]
        APIKeys[API Key Management]
    end
    
    subgraph "Performance Layer"
        ModelCache[ML Model Caching]
        DataCache[Data Caching]
        ResponseCache[Response Caching]
        LoadBalancing[Load Balancing]
    end
    
    subgraph "Monitoring Layer"
        Logging[Application Logging]
        Metrics[Performance Metrics]
        HealthChecks[Health Monitoring]
        ErrorTracking[Error Tracking]
    end
    
    subgraph "Application Core"
        API[FastAPI Application]
        Services[Core Services]
        Models[ML Models]
        Database[Data Layer]
    end
    
    CORS --> API
    RateLimit --> API
    InputValidation --> API
    APIKeys --> API
    
    ModelCache --> Services
    DataCache --> Services
    ResponseCache --> API
    
    API --> Logging
    Services --> Metrics
    API --> HealthChecks
    Services --> ErrorTracking
    
    API --> Services
    Services --> Models
    Services --> Database
```