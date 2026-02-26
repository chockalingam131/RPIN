## AWS Deployment Guide for RPIN

Complete guide for deploying the Rural Producer Intelligence Network to AWS.

## 🎯 Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended for Hackathon)
**Best for**: Quick deployment, automatic scaling, easy management
**Cost**: ~$10-20/month (free tier eligible)
**Difficulty**: Easy

### Option 2: AWS ECS with Fargate
**Best for**: Production-ready containerized deployment
**Cost**: ~$15-30/month
**Difficulty**: Medium

### Option 3: AWS Lambda + API Gateway (Serverless)
**Best for**: Cost optimization, pay-per-use
**Cost**: ~$5-10/month (mostly free tier)
**Difficulty**: Medium-Hard

---

## 📦 Option 1: AWS Elastic Beanstalk Deployment

### Prerequisites

1. **AWS Account**: Sign up at https://aws.amazon.com
2. **AWS CLI**: Install from https://aws.amazon.com/cli/
3. **EB CLI**: Install Elastic Beanstalk CLI

```bash
pip install awsebcli
```

### Step 1: Prepare Backend for Deployment

Create `requirements.txt` (already exists in backend/)

Create `.ebignore` file:
```bash
cd backend
cat > .ebignore << EOF
venv/
__pycache__/
*.pyc
.env
logs/
*.db
.git/
EOF
```

Create `Procfile`:
```bash
cat > Procfile << EOF
web: uvicorn main:app --host 0.0.0.0 --port 8000
EOF
```

### Step 2: Initialize Elastic Beanstalk

```bash
cd backend

# Initialize EB application
eb init -p python-3.9 rpin-backend --region us-east-1

# Create environment
eb create rpin-env --instance-type t2.micro

# This will:
# - Create EC2 instance
# - Set up load balancer
# - Configure security groups
# - Deploy your application
```

### Step 3: Configure Environment Variables

```bash
# Set environment variables
eb setenv \
  OPENWEATHER_API_KEY=your_key_here \
  LLM_API_KEY=your_key_here \
  DATABASE_URL=sqlite:///./rpin.db \
  ALLOWED_ORIGINS=https://your-frontend-url.com
```

### Step 4: Deploy Updates

```bash
# Deploy new version
eb deploy

# Check status
eb status

# View logs
eb logs

# Open in browser
eb open
```

### Step 5: Deploy Frontend to S3 + CloudFront

```bash
# Create S3 bucket
aws s3 mb s3://rpin-frontend-bucket --region us-east-1

# Enable static website hosting
aws s3 website s3://rpin-frontend-bucket \
  --index-document index.html \
  --error-document index.html

# Update API URL in frontend/index.html
# Change API_BASE_URL to your EB URL

# Upload frontend
cd frontend
aws s3 sync . s3://rpin-frontend-bucket --acl public-read

# Get website URL
echo "http://rpin-frontend-bucket.s3-website-us-east-1.amazonaws.com"
```

### Step 6: Set Up CloudFront (Optional - for HTTPS)

1. Go to AWS CloudFront Console
2. Create Distribution
3. Origin Domain: Your S3 bucket website endpoint
4. Default Root Object: index.html
5. Create Distribution
6. Wait 15-20 minutes for deployment
7. Access via CloudFront URL

### Cost Estimate (Elastic Beanstalk)
- EC2 t2.micro: $8-10/month (free tier: 750 hours/month)
- Load Balancer: $16/month
- S3 Storage: $0.50/month
- CloudFront: $1-2/month
- **Total**: ~$10-20/month (mostly free tier eligible)

---

## 🐳 Option 2: AWS ECS with Fargate

### Step 1: Create Docker Images

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data models

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `backend/.dockerignore`:
```
venv/
__pycache__/
*.pyc
.env
logs/
*.db
.git/
```

### Step 2: Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name rpin-backend --region us-east-1

# Get login command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
cd backend
docker build -t rpin-backend .

# Tag image
docker tag rpin-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rpin-backend:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rpin-backend:latest
```

### Step 3: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name rpin-cluster --region us-east-1
```

### Step 4: Create Task Definition

Create `task-definition.json`:
```json
{
  "family": "rpin-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "rpin-backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rpin-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENWEATHER_API_KEY",
          "value": "your_key_here"
        },
        {
          "name": "LLM_API_KEY",
          "value": "your_key_here"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rpin-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register task:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Step 5: Create Service

```bash
# Create service
aws ecs create-service \
  --cluster rpin-cluster \
  --service-name rpin-service \
  --task-definition rpin-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Cost Estimate (ECS Fargate)
- Fargate vCPU: $10/month
- Fargate Memory: $5/month
- Load Balancer: $16/month
- S3 + CloudFront: $2/month
- **Total**: ~$30-35/month

---

## ⚡ Option 3: AWS Lambda + API Gateway (Serverless)

### Step 1: Install Serverless Framework

```bash
npm install -g serverless
```

### Step 2: Create Serverless Configuration

Create `backend/serverless.yml`:
```yaml
service: rpin-backend

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    OPENWEATHER_API_KEY: ${env:OPENWEATHER_API_KEY}
    LLM_API_KEY: ${env:LLM_API_KEY}

functions:
  api:
    handler: lambda_handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 512

plugins:
  - serverless-python-requirements
```

Create `backend/lambda_handler.py`:
```python
from mangum import Mangum
from main import app

handler = Mangum(app)
```

### Step 3: Deploy

```bash
cd backend
pip install mangum
serverless deploy
```

### Cost Estimate (Lambda)
- Lambda requests: $0.20/million requests
- Lambda compute: $0.0000166667/GB-second
- API Gateway: $3.50/million requests
- S3 + CloudFront: $2/month
- **Total**: ~$5-10/month (mostly free tier)

---

## 🔒 Security Best Practices

### 1. Environment Variables
Never commit API keys. Use AWS Secrets Manager:

```bash
# Store secret
aws secretsmanager create-secret \
  --name rpin/api-keys \
  --secret-string '{"OPENWEATHER_API_KEY":"xxx","LLM_API_KEY":"xxx"}'
```

### 2. HTTPS Only
- Use CloudFront for HTTPS
- Get free SSL certificate from AWS Certificate Manager

### 3. CORS Configuration
Update backend CORS to allow only your frontend domain:

```python
# In backend/app/core/config.py
ALLOWED_ORIGINS = [
    "https://your-cloudfront-domain.cloudfront.net",
    "https://your-custom-domain.com"
]
```

### 4. API Rate Limiting
Add rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/predict")
@limiter.limit("10/minute")
async def predict_market(request: Request, ...):
    ...
```

---

## 📊 Monitoring and Logging

### CloudWatch Logs

```bash
# View logs
aws logs tail /aws/elasticbeanstalk/rpin-env/var/log/web.stdout.log --follow

# Or for ECS
aws logs tail /ecs/rpin-backend --follow
```

### CloudWatch Metrics
- Monitor CPU usage
- Monitor memory usage
- Monitor request count
- Set up alarms for errors

### Cost Monitoring
- Enable AWS Cost Explorer
- Set up billing alerts
- Monitor daily costs

---

## 🚀 CI/CD Pipeline (Optional)

### Using GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Deploy to Elastic Beanstalk
      run: |
        cd backend
        eb deploy rpin-env
```

---

## 🔄 Scaling Configuration

### Auto Scaling (Elastic Beanstalk)

```bash
# Configure auto scaling
eb config

# Add to configuration:
aws:autoscaling:asg:
  MinSize: 1
  MaxSize: 4
aws:autoscaling:trigger:
  MeasureName: CPUUtilization
  Statistic: Average
  Unit: Percent
  UpperThreshold: 80
  LowerThreshold: 20
```

---

## 💰 Cost Optimization Tips

1. **Use Free Tier**: Most services have 12-month free tier
2. **Right-size Instances**: Start with t2.micro, scale up if needed
3. **Use Spot Instances**: For non-critical workloads
4. **Enable Auto Scaling**: Scale down during low traffic
5. **Use CloudFront Caching**: Reduce backend requests
6. **Monitor Costs**: Set up billing alerts

---

## 🆘 Troubleshooting

### Backend Not Starting
```bash
# Check logs
eb logs

# SSH into instance
eb ssh

# Check application logs
tail -f /var/log/web.stdout.log
```

### CORS Errors
- Verify ALLOWED_ORIGINS in backend config
- Check CloudFront/S3 CORS configuration

### Database Issues
- For production, use RDS instead of SQLite
- Configure database connection in environment variables

### High Costs
- Check CloudWatch metrics
- Review auto-scaling configuration
- Consider serverless (Lambda) for low traffic

---

## 📝 Post-Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] API endpoints working
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] HTTPS enabled
- [ ] Monitoring configured
- [ ] Billing alerts set up
- [ ] Backup strategy in place
- [ ] Documentation updated with URLs

---

## 🎯 Quick Deployment Summary

**For Hackathon Demo (Fastest)**:
```bash
# Backend
cd backend
eb init -p python-3.9 rpin-backend
eb create rpin-env
eb setenv OPENWEATHER_API_KEY=xxx LLM_API_KEY=xxx

# Frontend
cd frontend
aws s3 mb s3://rpin-frontend
aws s3 sync . s3://rpin-frontend --acl public-read
```

**URLs**:
- Backend: `eb open` (will show URL)
- Frontend: `http://rpin-frontend.s3-website-us-east-1.amazonaws.com`

---

## 📚 Additional Resources

- [AWS Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/)
- [AWS ECS Docs](https://docs.aws.amazon.com/ecs/)
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 Success!

Your RPIN application is now deployed on AWS and accessible worldwide!

**Next Steps**:
1. Test all functionality
2. Share URLs with hackathon judges
3. Monitor performance
4. Gather user feedback
5. Iterate and improve
