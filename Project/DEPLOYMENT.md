# 🚀 Deployment Guide

Avalanche Intelligence Pro - Production Deployment Instructions

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Streamlit Cloud](#streamlit-cloud)
4. [Heroku](#heroku)
5. [AWS](#aws)
6. [GCP](#gcp)
7. [Azure](#azure)
8. [Production Checklist](#production-checklist)

---

## Local Development

### Setup
```bash
# Clone repository
git clone https://github.com/username/avalanche-intelligence.git
cd avalanche-intelligence/Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Development Server Options
```bash
# Default (localhost:8501)
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502

# Disable browser auto-open
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

---

## Docker Deployment

### Build Docker Image
```bash
# Build
docker build -t avalanche-intelligence-pro:latest .

# Build with specific version
docker build -t avalanche-intelligence-pro:v2.0 -t avalanche-intelligence-pro:latest .

# Build for ARM64 (Apple Silicon)
docker buildx build --platform linux/amd64,linux/arm64 -t avalanche-intelligence-pro:latest .
```

### Run Docker Container
```bash
# Basic run
docker run -p 8501:8501 avalanche-intelligence-pro:latest

# With volume mount for data persistence
docker run -p 8501:8501 -v $(pwd):/app avalanche-intelligence-pro:latest

# With environment variables
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_HEADLESS=true \
  avalanche-intelligence-pro:latest

# Daemonized (background)
docker run -d --name avalanche-pro -p 8501:8501 avalanche-intelligence-pro:latest

# View logs
docker logs -f avalanche-pro

# Stop container
docker stop avalanche-pro
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  avalanche-pro:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Run with: `docker-compose up -d`

---

## Streamlit Cloud (Recommended for MVP)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy Avalanche Intelligence Pro v2.0"
   git push origin main
   ```

2. **Connect Repository**
   - Go to [Streamlit Cloud](https://share.streamlit.io)
   - Click "New app"
   - Select GitHub repository and branch
   - Set main file path: `Project/app.py`

3. **Configure Secrets** (if needed)
   - Create `.streamlit/secrets.toml`:
   ```toml
   [database]
   url = "postgresql://..."
   
   [api]
   key = "your-api-key"
   ```

4. **Deploy**
   - Click "Deploy"
   - App will be live at `https://your-app-name.streamlit.app`

### Streamlit Cloud Advantages
✅ Free tier available  
✅ Auto-deploys from GitHub  
✅ Built-in SSL/HTTPS  
✅ Easy scaling  
✅ No DevOps needed  

---

## Heroku Deployment

### Setup

1. **Create Procfile**
   ```
   web: streamlit run Project/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create runtime.txt**
   ```
   python-3.11.0
   ```

3. **Create app.json**
   ```json
   {
     "name": "Avalanche Intelligence Pro",
     "description": "Enterprise avalanche analytics platform",
     "repository": "https://github.com/username/avalanche-intelligence",
     "keywords": ["streamlit", "avalanche", "analytics", "machine-learning"]
   }
   ```

### Deploy
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create avalanche-intelligence-pro

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Scale dynos
heroku scale web=2
```

### Heroku Cost Estimate
- Free tier: $0 (limited resources, sleeps after 30 min inactivity)
- Hobby tier: $7/month (always on)
- Standard tier: $25+/month (production)

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 avalanche-intelligence-pro

# Create environment
eb create avalanche-pro-env

# Deploy updates
git add .
git commit -m "Update"
eb deploy

# Monitor
eb open
eb logs
```

### Option 2: AWS App Runner

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [account-id].dkr.ecr.us-east-1.amazonaws.com

docker tag avalanche-intelligence-pro:latest [account-id].dkr.ecr.us-east-1.amazonaws.com/avalanche-pro:latest

docker push [account-id].dkr.ecr.us-east-1.amazonaws.com/avalanche-pro:latest

# Create App Runner service via AWS Console
# - Source: ECR repository
# - Image: your pushed image
# - Port: 8501
```

### Option 3: AWS Lambda + API Gateway (Serverless)
- Not ideal for Streamlit (stateful, long-running)
- Use ECS Fargate or Beanstalk instead

### AWS Cost Estimate
- Elastic Beanstalk: $20-100/month
- App Runner: $1-30/month
- EC2 instance: $10-50+/month

---

## GCP Deployment

### Cloud Run (Recommended)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Configure
gcloud config set project avalanche-intelligence

# Build image
gcloud builds submit --tag gcr.io/avalanche-intelligence/pro

# Deploy
gcloud run deploy avalanche-pro \
  --image gcr.io/avalanche-intelligence/pro:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi \
  --timeout 3600
```

### Cloud App Engine
```yaml
# app.yaml
runtime: python311

entrypoint: streamlit run app.py --server.port 8080

env: standard

env_variables:
  STREAMLIT_SERVER_HEADLESS: "true"
  STREAMLIT_SERVER_PORT: "8080"
```

Deploy: `gcloud app deploy`

### GCP Cost Estimate
- Cloud Run: $0.20-1.50/GB-hour (very cost-effective)
- App Engine: $14/month minimum
- Compute Engine: $20-100+/month

---

## Azure Deployment

### Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name avalanche-pro --location eastus

# Create container registry
az acr create --resource-group avalanche-pro \
  --name avalanchepro --sku Basic

# Build image
az acr build --registry avalanchepro \
  --image avalanche-pro:latest .

# Deploy container
az container create \
  --resource-group avalanche-pro \
  --name avalanche-pro \
  --image avalanchepro.azurecr.io/avalanche-pro:latest \
  --cpu 1 --memory 2 \
  --registry-login-server avalanchepro.azurecr.io \
  --registry-username [username] \
  --registry-password [password] \
  --ports 8501 \
  --dns-name-label avalanche-pro
```

### Azure App Service

```bash
# Create app service plan
az appservice plan create --name avalanche-plan \
  --resource-group avalanche-pro --sku B1 --is-linux

# Create web app
az webapp create --resource-group avalanche-pro \
  --plan avalanche-plan \
  --name avalanche-pro \
  --deployment-container-image-name-user-provided
```

### Azure Cost Estimate
- Container Instances: $0.0015/GB-second (~$30-50/month)
- App Service: $10-100+/month
- Functions: $0.20 per 1M executions

---

## Production Checklist

### Pre-Deployment
- [ ] All tests pass locally (`pytest`)
- [ ] Code formatted with `black`
- [ ] Linting passed (`pylint`)
- [ ] No security issues (`bandit`, `safety`)
- [ ] requirements.txt updated
- [ ] Data files included/accessible
- [ ] Environment variables documented
- [ ] Version number updated in code

### Security
- [ ] Remove debug logging in production
- [ ] Set `STREAMLIT_LOGGER_LEVEL=error`
- [ ] Enable HTTPS/SSL
- [ ] Use secrets manager for credentials
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Input validation active
- [ ] SQL injection prevention (if applicable)

### Performance
- [ ] Cache enabled for data loading
- [ ] Model training optimized
- [ ] Image size optimized
- [ ] Database indexes created (if applicable)
- [ ] CDN configured for static assets
- [ ] Load testing completed
- [ ] Monitoring alerts set up
- [ ] Autoscaling configured

### Monitoring & Logging
- [ ] Application monitoring (e.g., DataDog, New Relic)
- [ ] Error tracking (e.g., Sentry)
- [ ] Performance monitoring
- [ ] Log aggregation (e.g., CloudWatch, ELK)
- [ ] Health check endpoint
- [ ] Uptime monitoring
- [ ] Alert notifications configured
- [ ] Backup strategy in place

### Documentation
- [ ] README updated
- [ ] API documentation complete
- [ ] Deployment guide finalized
- [ ] Troubleshooting guide included
- [ ] Runbook for common issues
- [ ] Change log maintained

### Operations
- [ ] Rollback procedure documented
- [ ] Update strategy defined
- [ ] Maintenance window scheduled
- [ ] Incident response plan ready
- [ ] Access control configured
- [ ] Backup & disaster recovery tested
- [ ] Cost monitoring enabled
- [ ] Support contacts documented

---

## Environment Variables

### Required
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_LOGGER_LEVEL=info
```

### Optional
```bash
export MAX_UPLOAD_SIZE=200
export CACHE_TTL=3600
export DB_URL="postgresql://..."
export API_KEY="your-key"
export ENVIRONMENT="production"
```

---

## Scaling Strategies

### Horizontal Scaling (Multiple Instances)
- Use load balancer (AWS ALB, GCP LB, etc.)
- Deploy multiple container instances
- Share data via central database
- Session affinity for Streamlit

### Vertical Scaling (Larger Instances)
- Increase CPU/Memory allocation
- Use caching for ML models
- Optimize data loading
- Monitor resource usage

### Caching Strategy
```python
# In-memory cache for expensive operations
@st.cache_data(ttl=3600)
def train_ensemble_model():
    # ... training code ...
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs container-id

# Run interactively
docker run -it avalanche-intelligence-pro:latest bash

# Check dependencies
pip freeze | grep -E 'streamlit|pandas|scikit'
```

### Port already in use
```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 PID  # macOS/Linux
taskkill /PID 1234  # Windows
```

### Out of memory
- Reduce model size (fewer estimators)
- Enable streaming processing
- Increase container memory limits
- Use smaller batch sizes

### Slow performance
- Profile code with `py-spy`
- Enable caching (`@st.cache_data`)
- Optimize data loading
- Use async operations where possible

---

## Support

For deployment issues:
1. Check logs first
2. Review [Streamlit docs](https://docs.streamlit.io)
3. Check [GitHub Issues](https://github.com/username/avalanche-intelligence/issues)
4. Contact support team

---

**Last Updated**: 2026-09-01  
**Version**: 2.0.0
