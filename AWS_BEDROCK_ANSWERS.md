# AWS Bedrock Integration - Quick Answers

## Question 1: What's the specific GenAI model you're using?

### Primary Model: **Amazon Titan Text G1 - Express**

**Purpose**: Generate farmer-friendly explanations for market recommendations

**Why Titan Text Express**:
- **Cost-Effective**: $0.0008 per 1K input tokens, $0.0016 per 1K output tokens
- **Fast**: Low latency (<1 second) for real-time recommendations
- **Multilingual**: Supports Tamil, Hindi, Telugu for rural farmers
- **Context**: 8K token window - perfect for our use case
- **Integration**: Native AWS service, seamless with our stack

**Specific Use Cases**:
1. **Natural Language Explanations**: Convert "₹20,800 profit, 5.2% spoilage risk, 80km distance" into "Selling in Madurai after 3 days gives ₹20,800 profit, ₹7,300 more than local market due to rising prices and lower spoilage risk"

2. **Multilingual Support**: Generate same explanation in Tamil/Hindi for rural farmers

3. **Risk Communication**: Explain complex factors (weather, spoilage, transport) in simple terms

4. **Personalized Advice**: Contextual recommendations based on crop type, season, and market conditions

**Example Bedrock API Call**:
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

prompt = f"""Generate a simple explanation for a farmer:
- Crop: Tomato, 1000 kg from Theni
- Best Market: Madurai Mandi
- Profit: ₹20,800 (₹7,300 more than Coimbatore)
- Price: ₹28.50/kg, Demand: High
- Distance: 80 km, Spoilage Risk: 5.2%

Explain in simple English why this is best, under 100 words."""

response = bedrock.invoke_model(
    modelId='amazon.titan-text-express-v1',
    body=json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 200,
            "temperature": 0.7,
            "topP": 0.9
        }
    })
)
```

### Secondary Model: **Anthropic Claude 3 Haiku** (via Bedrock)

**Purpose**: Advanced market analysis and insights (premium feature)

**Why Claude 3 Haiku**:
- **Reasoning**: Better for complex market trend analysis
- **Accuracy**: Higher quality explanations for detailed insights
- **Cost**: $0.00025 per 1K input, $0.00125 per 1K output
- **Structured Output**: Better JSON formatting for API responses

**Use Cases**:
- Detailed market trend analysis
- Seasonal farming advice
- Complex risk assessments
- Comparative market analysis

### Tertiary Model: **Amazon Titan Embeddings G1 - Text**

**Purpose**: Semantic search and recommendation enhancement

**Why Titan Embeddings**:
- **Vector Search**: Find similar historical scenarios
- **Recommendations**: Suggest alternative crops/markets
- **Cost**: $0.0001 per 1K tokens
- **Dimension**: 1536-dimensional embeddings

**Use Cases**:
- "Farmers like you who sold tomatoes in March got best results in Chennai"
- "Similar weather conditions last year led to 15% higher prices"
- Crop recommendation based on historical success patterns

---

## Question 2: What's your data strategy?

### Data Sources

#### Real-Time Data (AWS Lambda + S3)
1. **AGMARKNET API** (Government of India)
   - Daily mandi prices for 300+ markets, 100+ commodities
   - 5+ years historical data
   - Update: Daily at 6 AM via Lambda
   - Storage: S3 (raw) → RDS (processed)

2. **OpenWeather API**
   - Current weather + 7-day forecasts
   - 1000+ locations in India
   - Update: Every 6 hours via Lambda
   - Storage: ElastiCache (hot) + RDS (historical)

3. **Static Data**
   - Crop database (shelf life, handling)
   - Market information (capacity, location)
   - Transport network (distances, costs)
   - Storage: S3 + RDS

### AWS Storage Architecture

```
┌─────────────────────────────────────────────────┐
│              Amazon S3 (Data Lake)              │
├─────────────────────────────────────────────────┤
│ • Raw Data: AGMARKNET, Weather (JSON/Parquet)  │
│ • Processed Data: Aggregated, cleaned          │
│ • ML Models: Trained models (.pkl files)       │
│ • Cost: $0.023/GB/month                        │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│         Amazon RDS PostgreSQL (Structured)      │
├─────────────────────────────────────────────────┤
│ • Historical Prices (indexed by date/market)   │
│ • Weather Cache (6-hour TTL)                   │
│ • Prediction Logs (audit trail)                │
│ • User Feedback (for model improvement)        │
│ • Cost: $15-30/month (db.t3.micro)             │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│      Amazon ElastiCache Redis (Hot Cache)      │
├─────────────────────────────────────────────────┤
│ • Price Predictions (1-hour TTL)               │
│ • Weather Forecasts (6-hour TTL)               │
│ • Market Recommendations (30-min TTL)          │
│ • Cost: $15/month (cache.t3.micro)             │
└─────────────────────────────────────────────────┘
```

### Data Processing Pipeline

```
External APIs → Lambda (Ingestion) → S3 (Raw Data)
                                        ↓
                          Lambda (ETL) → S3 (Processed)
                                        ↓
                                  RDS (Structured)
                                        ↓
                              ElastiCache (Cache)
                                        ↓
                          FastAPI + Bedrock (Application)
                                        ↓
                                  CloudFront (CDN)
                                        ↓
                                    Users
```

### Lambda Functions (Serverless Processing)

1. **Data Ingestion Lambda**
   - Trigger: CloudWatch Events (daily 6 AM)
   - Function: Fetch AGMARKNET data
   - Duration: 5 minutes
   - Cost: Free tier (1M requests/month)

2. **Weather Update Lambda**
   - Trigger: CloudWatch Events (every 6 hours)
   - Function: Fetch weather forecasts
   - Duration: 2 minutes
   - Cost: Free tier

3. **ML Training Lambda**
   - Trigger: CloudWatch Events (weekly)
   - Function: Retrain models on new data
   - Duration: 30 minutes
   - Memory: 3008 MB
   - Cost: ~$2/month

### Data Governance

**Security**:
- S3 encryption at rest (SSE-S3)
- RDS encryption enabled
- TLS 1.2+ for data in transit
- IAM roles with least privilege
- API keys in AWS Secrets Manager

**Compliance**:
- No PII collection (farmer-friendly)
- 5-year data retention
- CloudTrail audit logs
- Automated daily backups

**Monitoring**:
- CloudWatch metrics for all services
- Alarms for data freshness
- Cost tracking per service
- Data quality checks

### Cost Breakdown

**Storage**:
- S3 (10 GB): $0.23/month
- RDS (20 GB): $15/month
- ElastiCache: $15/month
- **Total**: ~$30/month

**Processing**:
- Lambda (1M requests): Free tier
- Data transfer: $1-2/month
- **Total**: ~$2/month

**Total Data Infrastructure**: ~$32/month

---

## Question 3: What is your "24-hour Goal"?

### Goal: **Production-Ready RPIN with Full Bedrock Integration**

### Hour-by-Hour Breakdown

#### Hours 0-4: Infrastructure Setup
**Milestone**: Backend deployed, Bedrock enabled, database initialized

✅ **Hour 1**: AWS Account Setup
- Enable Bedrock in us-east-1
- Request model access (Titan Text, Claude, Embeddings)
- Create IAM roles with Bedrock permissions
- Configure AWS CLI

✅ **Hour 2-3**: Backend Deployment
- Deploy FastAPI to Elastic Beanstalk
- Set up RDS PostgreSQL
- Initialize database schema
- Configure environment variables

✅ **Hour 4**: Data Pipeline
- Create S3 buckets
- Deploy Lambda functions
- Test AGMARKNET data fetch
- Verify data storage

#### Hours 4-8: Bedrock Integration
**Milestone**: AI-powered explanations working

✅ **Hour 5**: Bedrock Client Implementation
```python
# Integrate Titan Text Express
bedrock_client = boto3.client('bedrock-runtime')
explanation = bedrock_client.invoke_model(
    modelId='amazon.titan-text-express-v1',
    body=json.dumps(prompt_config)
)
```

✅ **Hour 6-7**: Update Explanation Service
- Replace template-based with Bedrock
- Add fallback mechanism
- Test with sample predictions
- Verify response quality

✅ **Hour 8**: Multilingual Support
- Add Tamil/Hindi prompts
- Test language switching
- Update API with language parameter

#### Hours 8-12: Frontend & Testing
**Milestone**: End-to-end system working

✅ **Hour 9**: Frontend Deployment
- Deploy to S3
- Configure CloudFront
- Update API URLs
- Test HTTPS access

✅ **Hour 10-11**: End-to-End Testing
- Test 3 demo scenarios
- Verify Bedrock explanations
- Check response times (<3 sec)
- Test error handling

✅ **Hour 12**: Performance Optimization
- Enable ElastiCache
- Optimize database queries
- Configure CDN caching
- Load test (50 concurrent users)

#### Hours 12-16: Data Population
**Milestone**: Historical data loaded, models trained

✅ **Hour 13-14**: Historical Data Import
- Fetch 30 days AGMARKNET data
- Import to RDS
- Create indexes
- Verify data quality

✅ **Hour 15**: Weather Data Setup
- Fetch current weather
- Fetch 7-day forecasts
- Populate cache
- Test integration

✅ **Hour 16**: ML Model Training
- Train price predictor
- Train demand classifier
- Validate accuracy
- Deploy to S3

#### Hours 16-20: Monitoring & Security
**Milestone**: Production-ready monitoring

✅ **Hour 17**: CloudWatch Setup
- Configure logs
- Create dashboards
- Set up alarms
- Test notifications

✅ **Hour 18**: Cost Monitoring
- Enable Cost Explorer
- Set billing alerts
- Tag all resources
- Create cost dashboard

✅ **Hour 19-20**: Security Audit
- Review IAM permissions
- Enable CloudTrail
- Configure security groups
- Run security scan

#### Hours 20-24: Documentation & Demo
**Milestone**: Demo-ready with documentation

✅ **Hour 21-22**: Documentation
- Update README with URLs
- Document Bedrock integration
- Create API examples
- Update deployment guide

✅ **Hour 23**: Demo Preparation
- Record 3-minute video
- Create presentation (10 slides)
- Test all scenarios
- Prepare Q&A

✅ **Hour 24**: Final Validation
- End-to-end system test
- Performance benchmark
- Security checklist
- Backup verification

### Success Criteria (24-Hour Checkpoint)

**Functional** ✅:
- Backend: https://rpin-env.us-east-1.elasticbeanstalk.com
- Frontend: https://d1234567890.cloudfront.net
- API Docs: https://rpin-env.us-east-1.elasticbeanstalk.com/docs
- Bedrock explanations working
- All 3 demo scenarios passing
- Response time <3 seconds

**Data** ✅:
- 30 days historical prices loaded
- Weather data for 8 villages
- All static data loaded
- Database indexed

**Performance** ✅:
- 50 concurrent users supported
- API response <2 seconds
- Bedrock latency <1 second
- 99.9% uptime

**Monitoring** ✅:
- CloudWatch dashboards live
- Alarms configured
- Cost tracking enabled
- Logs searchable

### Deliverables After 24 Hours

1. **Live Application**
   - Production URLs (backend + frontend)
   - API documentation
   - Working demo scenarios

2. **GitHub Repository**
   - Complete source code
   - Deployment scripts
   - Comprehensive documentation

3. **Demo Video** (3 minutes)
   - Problem statement
   - Live demo
   - Bedrock showcase
   - Architecture overview

4. **Presentation** (10 slides)
   - Problem & solution
   - Technical architecture
   - Bedrock integration
   - Data strategy
   - Social impact
   - Cost analysis

5. **Metrics Dashboard**
   - API requests
   - Response times
   - Bedrock usage
   - Cost breakdown

### Cost Summary

**Monthly Costs**:
- Infrastructure (EB, RDS, Cache, S3): $45-50
- Bedrock (Titan Text): $10
- External APIs: Free
- **Total**: ~$55-60/month

**With AWS Credits**: FREE for 12 months! 🎉

### Key Differentiators

✅ **Real GenAI**: Not just API calls, actual Bedrock integration
✅ **Production-Ready**: In 24 hours, not weeks
✅ **Scalable**: Auto-scaling from day 1
✅ **Cost-Effective**: <$60/month, free with credits
✅ **Social Impact**: Helping rural farmers maximize profits
✅ **Data-Driven**: Comprehensive AWS data strategy

---

## Summary

**Model**: Amazon Titan Text G1 - Express (primary) + Claude 3 Haiku (advanced) + Titan Embeddings (search)

**Data**: S3 (data lake) + RDS (structured) + ElastiCache (cache) + Lambda (processing)

**24-Hour Goal**: Production-ready RPIN with full Bedrock integration, 30 days historical data, complete monitoring, and demo-ready documentation

**Ready to deploy and make an impact!** 🚀
