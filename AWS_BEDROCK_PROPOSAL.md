# RPIN - AWS Bedrock Integration Proposal

## 1. GenAI Model Strategy via AWS Bedrock

### Primary Model: Amazon Titan Text G1 - Express
**Purpose**: Natural language explanation generation for market recommendations

**Why This Model**:
- **Cost-Effective**: $0.0008 per 1K input tokens, $0.0016 per 1K output tokens
- **Fast Response**: Low latency for real-time recommendations
- **Multilingual**: Supports regional Indian languages (Tamil, Hindi, Telugu)
- **Context Window**: 8K tokens - sufficient for our use case
- **AWS Native**: Seamless integration with other AWS services

**Use Cases in RPIN**:
1. **Farmer-Friendly Explanations**: Convert technical predictions into simple language
2. **Multilingual Support**: Generate explanations in local languages
3. **Contextual Recommendations**: Provide personalized advice based on crop, location, and market conditions
4. **Risk Communication**: Explain spoilage risks and weather impacts clearly

**Example Prompt**:
```
Generate a simple explanation for a farmer in Tamil Nadu:
- Crop: Tomato, 1000 kg
- Village: Theni
- Best Market: Madurai Mandi
- Expected Profit: ₹20,800
- Price: ₹28.50/kg
- Spoilage Risk: 5.2%
- Distance: 80 km

Explain in simple English why this is the best choice, mentioning:
1. Profit comparison with other markets
2. Key factors (price, distance, spoilage)
3. Practical advice for transport

Keep it under 100 words, farmer-friendly language.
```

### Secondary Model: Anthropic Claude 3 Haiku (via Bedrock)
**Purpose**: Advanced analysis and insights for premium features

**Why This Model**:
- **Reasoning**: Better for complex market analysis
- **Accuracy**: Higher quality explanations
- **Structured Output**: Better JSON formatting for API responses
- **Cost**: $0.00025 per 1K input tokens, $0.00125 per 1K output tokens

**Use Cases**:
1. **Market Trend Analysis**: Analyze historical patterns
2. **Risk Assessment**: Complex spoilage risk explanations
3. **Seasonal Insights**: Provide seasonal farming advice
4. **Comparative Analysis**: Detailed market comparisons

### Tertiary Model: Amazon Titan Embeddings G1 - Text
**Purpose**: Semantic search and recommendation enhancement

**Why This Model**:
- **Vector Embeddings**: For similar crop/market recommendations
- **Search**: Find similar historical scenarios
- **Cost**: $0.0001 per 1K tokens
- **Dimension**: 1536 dimensions

**Use Cases**:
1. **Similar Scenarios**: Find similar past predictions
2. **Crop Recommendations**: Suggest alternative crops
3. **Market Clustering**: Group similar markets
4. **Historical Search**: Search past successful transactions

---

## 2. Data Strategy on AWS

### Data Sources

#### A. Real-Time Data Sources
1. **AGMARKNET API** (Government of India)
   - Daily mandi prices for 300+ markets
   - 100+ commodities
   - Historical data: 5+ years
   - Format: JSON/CSV
   - Update Frequency: Daily

2. **OpenWeather API**
   - Current weather + 7-day forecasts
   - Temperature, humidity, precipitation
   - 1000+ locations in India
   - Update Frequency: Every 3 hours

3. **India Meteorological Department (IMD)**
   - Extended weather forecasts
   - Seasonal predictions
   - Agricultural advisories

#### B. Static Data Sources
1. **Crop Database**
   - Shelf life data
   - Optimal storage conditions
   - Handling requirements
   - Source: Agricultural universities, ICAR

2. **Market Information**
   - Market locations and capacity
   - Operating days and hours
   - Contact information
   - Source: State agricultural departments

3. **Transport Network**
   - Village-to-market distances
   - Road conditions
   - Transport costs
   - Source: Google Maps API, government data

### Data Storage on AWS

#### Primary Storage: Amazon S3
**Structure**:
```
s3://rpin-data-bucket/
├── raw/
│   ├── agmarknet/
│   │   ├── daily/YYYY-MM-DD.json
│   │   └── historical/crop_market_YYYY.parquet
│   ├── weather/
│   │   ├── forecasts/location_YYYY-MM-DD.json
│   │   └── historical/location_YYYY.parquet
│   └── static/
│       ├── crops.json
│       ├── markets.json
│       └── distances.json
├── processed/
│   ├── price_trends/
│   ├── demand_patterns/
│   └── ml_features/
└── models/
    ├── price_predictor_v1.pkl
    ├── demand_classifier_v1.pkl
    └── embeddings/
```

**Why S3**:
- **Cost**: $0.023 per GB/month (Standard)
- **Durability**: 99.999999999% (11 9's)
- **Scalability**: Unlimited storage
- **Integration**: Works with all AWS services

#### Database: Amazon RDS (PostgreSQL)
**Schema**:
```sql
-- Historical Prices
CREATE TABLE historical_prices (
    id SERIAL PRIMARY KEY,
    market_id VARCHAR(50),
    crop_id VARCHAR(50),
    date DATE,
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2),
    modal_price DECIMAL(10,2),
    arrivals_tons DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_market_crop_date (market_id, crop_id, date)
);

-- Weather Cache
CREATE TABLE weather_cache (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100),
    date DATE,
    temperature_celsius DECIMAL(5,2),
    humidity_percent DECIMAL(5,2),
    precipitation_mm DECIMAL(5,2),
    fetched_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_location_date (location, date)
);

-- Predictions Log
CREATE TABLE prediction_logs (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(100) UNIQUE,
    village_location VARCHAR(100),
    crop_type VARCHAR(50),
    quantity_kg DECIMAL(10,2),
    harvest_date DATE,
    best_market_id VARCHAR(50),
    best_market_profit DECIMAL(12,2),
    total_markets_analyzed INT,
    response_time_ms DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- User Feedback
CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    prediction_id INT REFERENCES prediction_logs(id),
    actual_market VARCHAR(50),
    actual_price DECIMAL(10,2),
    actual_profit DECIMAL(12,2),
    satisfaction_score INT CHECK (satisfaction_score BETWEEN 1 AND 5),
    comments TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Why RDS PostgreSQL**:
- **ACID Compliance**: Data integrity
- **Complex Queries**: JOIN operations, aggregations
- **Backup**: Automated backups
- **Scaling**: Read replicas for high traffic
- **Cost**: $15-30/month for db.t3.micro

#### Caching: Amazon ElastiCache (Redis)
**Cache Strategy**:
```python
# Price predictions cache (1 hour TTL)
cache_key = f"price:{crop_id}:{market_id}:{date}"

# Weather forecasts cache (6 hours TTL)
cache_key = f"weather:{location}:{date}"

# Market recommendations cache (30 minutes TTL)
cache_key = f"recommendation:{village}:{crop}:{quantity}:{date}"
```

**Why ElastiCache**:
- **Speed**: Sub-millisecond latency
- **Reduce API Calls**: Save on external API costs
- **Scalability**: Handle high traffic
- **Cost**: $15/month for cache.t3.micro

#### Vector Database: Amazon OpenSearch Service
**Purpose**: Store embeddings for semantic search

**Use Cases**:
- Similar scenario search
- Crop recommendations
- Market clustering
- Historical pattern matching

**Cost**: $20-30/month for small instance

### Data Processing Pipeline

#### AWS Lambda Functions
1. **Data Ingestion Lambda**
   - Trigger: CloudWatch Events (daily at 6 AM)
   - Function: Fetch AGMARKNET data
   - Store: Raw data to S3
   - Duration: 5 minutes
   - Memory: 512 MB

2. **Data Processing Lambda**
   - Trigger: S3 event (new raw data)
   - Function: Clean, transform, aggregate
   - Store: Processed data to S3 + RDS
   - Duration: 10 minutes
   - Memory: 1024 MB

3. **Weather Update Lambda**
   - Trigger: CloudWatch Events (every 6 hours)
   - Function: Fetch weather forecasts
   - Store: Weather cache in RDS + ElastiCache
   - Duration: 2 minutes
   - Memory: 256 MB

4. **ML Model Training Lambda**
   - Trigger: CloudWatch Events (weekly)
   - Function: Retrain models on new data
   - Store: Updated models to S3
   - Duration: 30 minutes
   - Memory: 3008 MB

#### AWS Glue (Optional for Big Data)
**ETL Jobs**:
- Convert CSV to Parquet
- Aggregate historical data
- Feature engineering for ML
- Data quality checks

**Why Glue**:
- **Serverless**: No infrastructure management
- **Scalable**: Process large datasets
- **Cost**: Pay per job run

#### Amazon Kinesis (Future - Real-Time)
**For Real-Time Price Updates**:
- Stream: AGMARKNET price updates
- Process: Real-time aggregation
- Store: Hot data in ElastiCache
- Alert: Price spike notifications

### Data Flow Architecture

```
External APIs → Lambda (Ingestion) → S3 (Raw)
                                        ↓
                            Lambda (Processing) → S3 (Processed)
                                        ↓
                                    RDS (Structured)
                                        ↓
                            ElastiCache (Hot Cache)
                                        ↓
                            FastAPI (Application)
                                        ↓
                            Bedrock (Explanations)
                                        ↓
                                User (Frontend)
```

### Data Governance

#### Security
- **Encryption at Rest**: S3 SSE, RDS encryption
- **Encryption in Transit**: TLS 1.2+
- **Access Control**: IAM roles, least privilege
- **Secrets**: AWS Secrets Manager for API keys

#### Compliance
- **Data Privacy**: No PII collection
- **Data Retention**: 5 years for historical data
- **Audit Logs**: CloudTrail for all data access
- **Backup**: Daily automated backups

#### Monitoring
- **CloudWatch Metrics**: Storage usage, API calls
- **CloudWatch Alarms**: Data freshness, API failures
- **CloudWatch Logs**: All Lambda executions
- **Cost Explorer**: Track data storage costs

---

## 3. 24-Hour Goal (First Technical Milestone)

### Goal: Deploy Production-Ready RPIN with Bedrock Integration

**Timeline**: Within 24 hours of AWS credits activation

### Hour 0-4: Infrastructure Setup

**Milestone 1.1: AWS Account Configuration** (1 hour)
- ✅ Enable AWS Bedrock in us-east-1 region
- ✅ Request model access for:
  - Amazon Titan Text G1 - Express
  - Anthropic Claude 3 Haiku
  - Amazon Titan Embeddings G1
- ✅ Create IAM roles with Bedrock permissions
- ✅ Set up AWS CLI and credentials

**Milestone 1.2: Backend Deployment** (2 hours)
- ✅ Deploy FastAPI backend to Elastic Beanstalk
- ✅ Configure environment variables
- ✅ Set up RDS PostgreSQL database
- ✅ Initialize database schema
- ✅ Verify health endpoint

**Milestone 1.3: Data Pipeline Setup** (1 hour)
- ✅ Create S3 buckets for data storage
- ✅ Deploy Lambda functions for data ingestion
- ✅ Set up CloudWatch Events for scheduling
- ✅ Test AGMARKNET data fetch
- ✅ Verify data storage in S3 and RDS

### Hour 4-8: Bedrock Integration

**Milestone 2.1: Bedrock Client Setup** (1 hour)
```python
# backend/app/services/bedrock_client.py
import boto3
import json

class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )
        self.model_id = "amazon.titan-text-express-v1"
    
    def generate_explanation(self, prompt: str) -> str:
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 200,
                "temperature": 0.7,
                "topP": 0.9
            }
        })
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['results'][0]['outputText']
```

**Milestone 2.2: Update Explanation Service** (1 hour)
- ✅ Integrate Bedrock client
- ✅ Update explanation generation logic
- ✅ Add fallback to template-based
- ✅ Test with sample predictions

**Milestone 2.3: Multilingual Support** (2 hours)
- ✅ Add language parameter to API
- ✅ Create prompts for Tamil, Hindi
- ✅ Test multilingual explanations
- ✅ Update frontend with language selector

### Hour 8-12: Frontend Deployment

**Milestone 3.1: Frontend Deployment** (1 hour)
- ✅ Update API URL in frontend
- ✅ Deploy to S3 bucket
- ✅ Configure S3 for static website hosting
- ✅ Set up CloudFront distribution
- ✅ Configure custom domain (optional)

**Milestone 3.2: End-to-End Testing** (2 hours)
- ✅ Test all 3 demo scenarios
- ✅ Verify Bedrock explanations
- ✅ Test multilingual support
- ✅ Check response times (<3 seconds)
- ✅ Verify error handling

**Milestone 3.3: Performance Optimization** (1 hour)
- ✅ Enable ElastiCache for caching
- ✅ Optimize database queries
- ✅ Configure CloudFront caching
- ✅ Test under load (50 concurrent users)

### Hour 12-16: Data Population

**Milestone 4.1: Historical Data Import** (2 hours)
- ✅ Fetch 30 days of AGMARKNET data
- ✅ Import into RDS database
- ✅ Verify data quality
- ✅ Create indexes for performance

**Milestone 4.2: Weather Data Setup** (1 hour)
- ✅ Fetch current weather for all locations
- ✅ Fetch 7-day forecasts
- ✅ Store in cache and database
- ✅ Verify weather integration

**Milestone 4.3: ML Model Training** (1 hour)
- ✅ Train price predictor on historical data
- ✅ Train demand classifier
- ✅ Validate model accuracy
- ✅ Deploy models to S3

### Hour 16-20: Monitoring & Logging

**Milestone 5.1: CloudWatch Setup** (1 hour)
- ✅ Configure application logs
- ✅ Set up custom metrics
- ✅ Create dashboards
- ✅ Configure alarms for errors

**Milestone 5.2: Cost Monitoring** (1 hour)
- ✅ Enable Cost Explorer
- ✅ Set up billing alerts
- ✅ Tag all resources
- ✅ Create cost dashboard

**Milestone 5.3: Security Audit** (2 hours)
- ✅ Review IAM permissions
- ✅ Enable CloudTrail
- ✅ Configure security groups
- ✅ Enable AWS WAF (optional)
- ✅ Run security scan

### Hour 20-24: Documentation & Demo

**Milestone 6.1: Documentation Update** (2 hours)
- ✅ Update README with AWS URLs
- ✅ Document Bedrock integration
- ✅ Create API usage examples
- ✅ Update deployment guide

**Milestone 6.2: Demo Preparation** (1 hour)
- ✅ Create demo video (3 minutes)
- ✅ Prepare presentation slides
- ✅ Test all demo scenarios
- ✅ Prepare Q&A responses

**Milestone 6.3: Final Validation** (1 hour)
- ✅ End-to-end system test
- ✅ Performance benchmarking
- ✅ Security checklist
- ✅ Backup verification
- ✅ Disaster recovery test

### Success Criteria (24-Hour Checkpoint)

**Functional Requirements**:
- ✅ Backend deployed and accessible via HTTPS
- ✅ Frontend deployed with custom domain
- ✅ Bedrock integration working for explanations
- ✅ All 3 demo scenarios working
- ✅ Response time <3 seconds
- ✅ 99.9% uptime during testing

**Data Requirements**:
- ✅ 30 days of historical price data loaded
- ✅ Weather data for all 8 villages
- ✅ All static data (crops, markets, distances) loaded
- ✅ Database properly indexed

**Performance Requirements**:
- ✅ Handle 50 concurrent users
- ✅ API response time <2 seconds
- ✅ Bedrock explanation generation <1 second
- ✅ 95th percentile latency <3 seconds

**Monitoring Requirements**:
- ✅ CloudWatch dashboards configured
- ✅ Alarms set for critical metrics
- ✅ Cost tracking enabled
- ✅ Logs aggregated and searchable

**Documentation Requirements**:
- ✅ Deployment guide updated
- ✅ API documentation complete
- ✅ Demo video recorded
- ✅ Presentation ready

### Deliverables After 24 Hours

1. **Live Application**
   - Backend URL: https://rpin-env.us-east-1.elasticbeanstalk.com
   - Frontend URL: https://d1234567890.cloudfront.net
   - API Docs: https://rpin-env.us-east-1.elasticbeanstalk.com/docs

2. **GitHub Repository**
   - Complete source code
   - Deployment scripts
   - Documentation
   - Demo scenarios

3. **Demo Video** (3 minutes)
   - Problem statement
   - Live demo of 2 scenarios
   - Bedrock explanation showcase
   - Technical architecture overview

4. **Presentation Deck** (10 slides)
   - Problem and solution
   - Technical architecture
   - Bedrock integration
   - Data strategy
   - Social impact
   - Scalability
   - Cost analysis
   - Future roadmap

5. **Metrics Dashboard**
   - API request count
   - Response times
   - Bedrock API calls
   - Cost breakdown
   - User engagement

---

## Cost Breakdown (Monthly)

### AWS Services
- **Elastic Beanstalk (t2.micro)**: $8-10 (free tier)
- **RDS PostgreSQL (db.t3.micro)**: $15
- **ElastiCache (cache.t3.micro)**: $15
- **S3 Storage (10 GB)**: $0.23
- **CloudFront (10 GB transfer)**: $1
- **Lambda (1M requests)**: $0.20 (free tier)
- **CloudWatch**: $5
- **Total Infrastructure**: ~$45-50/month

### Bedrock Costs (Estimated)
- **Titan Text Express**: 
  - 1000 predictions/day × 200 tokens = 200K tokens/day
  - 6M tokens/month × $0.0016 = $9.60/month
- **Titan Embeddings** (optional):
  - 100 embeddings/day × 1K tokens = 100K tokens/day
  - 3M tokens/month × $0.0001 = $0.30/month
- **Total Bedrock**: ~$10/month

### External APIs
- **OpenWeather API**: Free tier (1000 calls/day)
- **AGMARKNET**: Free (government data)

### **Total Monthly Cost**: ~$55-60/month

### **With AWS Credits**: Effectively FREE for 12 months!

---

## Success Metrics

### Technical Metrics
- **Uptime**: 99.9%
- **Response Time**: <2 seconds (95th percentile)
- **Bedrock Latency**: <1 second
- **Error Rate**: <0.1%
- **API Success Rate**: >99%

### Business Metrics
- **Daily Active Users**: 100+ (target)
- **Predictions per Day**: 500+ (target)
- **User Satisfaction**: 4.5/5 (target)
- **Recommendation Accuracy**: 80%+ (target)

### Cost Metrics
- **Cost per Prediction**: <$0.02
- **Bedrock Cost per Prediction**: <$0.01
- **Infrastructure Cost per User**: <$0.50/month

---

## Risk Mitigation

### Technical Risks
1. **Bedrock API Limits**: Implement rate limiting and queuing
2. **Data Quality**: Validate all external data sources
3. **Model Accuracy**: Continuous monitoring and retraining
4. **Scalability**: Auto-scaling configured from day 1

### Operational Risks
1. **API Downtime**: Fallback to template-based explanations
2. **Cost Overrun**: Billing alarms and budget limits
3. **Security**: Regular security audits and updates
4. **Data Loss**: Automated backups and disaster recovery

---

## Conclusion

This 24-hour plan ensures a production-ready RPIN system with full Bedrock integration, comprehensive data strategy, and robust AWS infrastructure. The system will be ready to serve farmers with AI-powered market recommendations immediately after deployment.

**Key Differentiators**:
- ✅ Real GenAI integration (not just API calls)
- ✅ Comprehensive data strategy with AWS services
- ✅ Production-ready in 24 hours
- ✅ Scalable architecture
- ✅ Cost-effective solution
- ✅ Social impact focus

**Ready to deploy and make an impact!** 🚀
