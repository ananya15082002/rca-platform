# RCA Platform - Deployment Guide

## 🎯 Project Summary

The RCA Platform is a comprehensive cloud-hosted system that:

1. **Continuously monitors** error metrics from CubeAPM every 5 minutes
2. **Correlates data** by linking errors with traces and logs
3. **Performs RCA** using local LLMs for intelligent analysis (no API limits!)
4. **Sends alerts** via Google Chat for new errors
5. **Provides dashboard** with real-time visualization and drill-down capabilities

## 📊 Data Flow Architecture

```
CubeAPM Metrics → Error Cards → Traces → Spans → Logs → Local LLM Analysis → Database → Dashboard
     ↓
Google Chat Alerts ← RCA Reports ← PostgreSQL ← Correlation Data
```

## 🏗️ System Components

### Backend (FastAPI)
- **Database**: PostgreSQL with optimized indexes
- **Worker**: Background process running every 5 minutes
- **API**: RESTful endpoints for dashboard consumption
- **Local LLM Integration**: Uses local models for RCA analysis (no API limits!)
- **Alerting**: Google Chat webhook integration

### Frontend (React)
- **Dashboard**: Real-time error monitoring with charts
- **Detail Views**: Drill-down into traces, spans, logs, and RCA
- **Filtering**: By environment, service, and time window
- **Export**: Download complete correlation data as JSON

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone and setup
git clone <repository>
cd RCA_Agent_5xx_Error

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Configure environment
cp env.example .env
# Edit .env with your configuration
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb rca_platform

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/rca_platform
```

### 3. Test Setup

```bash
# Run setup test
python test_setup.py
```

### 4. Start Services

```bash
# Terminal 1: Backend API
python run_backend.py

# Terminal 2: Background Worker
python run_worker.py

# Terminal 3: Frontend
cd frontend && npm start
```

## 🌐 Deployment Options

### Option 1: Render.com (Recommended)

1. **Fork** this repository to your GitHub account
2. **Connect** to Render.com
3. **Create** new Web Service from GitHub
4. **Configure** environment variables in Render dashboard
5. **Deploy** automatically

**Required Environment Variables:**
- `DATABASE_URL` (PostgreSQL connection string)
- `GOOGLE_CHAT_WEBHOOK_URL` (Already configured)
- `METRIC_URL`, `TRACE_BASE_URL`, `LOGS_API_URL` (Already configured)

**No API keys needed!** The system uses local LLM models.

### Option 2: Railway.app

1. **Connect** GitHub repository to Railway
2. **Add** PostgreSQL database
3. **Set** environment variables
4. **Deploy** automatically

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and deploy
fly auth login
fly launch
fly deploy
```

### Option 4: Heroku

```bash
# Install Heroku CLI
# Create app and add PostgreSQL
heroku create rca-platform
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main
```

## 🤖 Local LLM Integration

The system uses local language models for RCA analysis:

- **No API Limits**: Unlimited analysis without external dependencies
- **Privacy**: All analysis happens locally
- **Cost Effective**: No API costs or rate limits
- **Reliable**: Works offline and doesn't depend on external services
- **Customizable**: Can switch between different local models

**Available Models:**
- `microsoft/DialoGPT-medium` (default) - Good for conversational analysis
- `gpt2` - Smaller, faster model
- `EleutherAI/gpt-neo-125M` - Good balance of speed and quality

The local LLM will be automatically downloaded on first run.

## 📱 Google Chat Integration

The system automatically sends structured alerts to Google Chat when new errors are detected:

```
🚨 [RCA Alert] New error detected!
Environment: prod | Service: api-gateway
Exception: 500 Internal Server Error
Count: 3
Time: 2025-01-27 14:30:00 - 14:35:00 IST
RCA: Database connection timeout causing 500 errors...
[Open Dashboard](https://your-dashboard-url.com/error/abc123)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GOOGLE_CHAT_WEBHOOK_URL` | Google Chat webhook URL | Yes |
| `METRIC_URL` | CubeAPM metrics endpoint | Yes |
| `TRACE_BASE_URL` | CubeAPM traces endpoint | Yes |
| `LOGS_API_URL` | Coralogix logs endpoint | Yes |
| `DASHBOARD_BASE_URL` | Your deployment URL | Yes |

**Note**: No API keys needed! The system uses local LLM models.

### Database Schema

The system creates these tables automatically:

- **error_metrics**: Error card data with timestamps
- **traces**: Trace IDs linked to error metrics  
- **spans**: Span metadata with operations and timing
- **logs**: Log data grouped by trace ID
- **rca_reports**: Local LLM analysis results

## 📊 API Endpoints

### Core Endpoints

- `GET /api/health` - Health check
- `GET /api/errors` - List error metrics (with filtering)
- `GET /api/errors/{id}` - Get error details
- `GET /api/errors/{id}/download` - Download correlation data
- `GET /api/stats` - Platform statistics
- `POST /api/trigger-cycle` - Manual ingestion trigger

### Query Parameters

- `hours` - Time window (1, 6, 24, 48 hours)
- `env` - Filter by environment
- `service` - Filter by service

## 🎯 Dashboard Features

### Main Dashboard
- **Real-time Statistics**: Error counts, traces, logs, RCA reports
- **Interactive Charts**: Environment and service breakdowns
- **Error Cards**: Clickable summaries with quick actions
- **Live Updates**: Auto-refresh every 5 minutes
- **Advanced Filtering**: By environment, service, time window

### Error Detail View
- **Overview Tab**: Summary statistics and RCA analysis
- **Traces Tab**: All trace IDs for the error
- **Spans Tab**: Detailed span information in table format
- **Logs Tab**: All related logs with JSON formatting
- **RCA Analysis Tab**: Local LLM-generated root cause analysis
- **Download**: Complete correlation data as JSON

## 🔍 Monitoring & Troubleshooting

### Health Checks

```bash
# Test API health
curl https://your-backend-url.com/api/health

# Test database connection
curl https://your-backend-url.com/api/stats
```

### Common Issues

1. **Database Connection**: Verify `DATABASE_URL` is correct
2. **Local LLM**: Check if models are downloading properly
3. **Google Chat**: Verify webhook URL is accessible
4. **CubeAPM**: Ensure endpoints are reachable

### Logs

```bash
# Backend logs
python run_backend.py

# Worker logs  
python run_worker.py

# Frontend logs
cd frontend && npm start
```

## 🚀 Production Checklist

- [ ] Environment variables configured
- [ ] Database created and accessible
- [ ] Google Chat webhook configured
- [ ] CubeAPM endpoints accessible
- [ ] Backend API deployed and running
- [ ] Background worker deployed and running
- [ ] Frontend deployed and accessible
- [ ] Health checks passing
- [ ] Test data ingestion cycle
- [ ] Verify Google Chat alerts working
- [ ] Local LLM models downloaded successfully

## 📞 Support

For deployment issues:

1. **Check logs** for error details
2. **Verify environment** variables are set correctly
3. **Test API endpoints** directly
4. **Review database** connectivity
5. **Check CubeAPM** endpoint accessibility
6. **Verify local LLM** model downloads

## 🎉 Success Metrics

Once deployed successfully, you should see:

- ✅ Backend API responding to health checks
- ✅ Background worker running every 5 minutes
- ✅ Dashboard displaying real-time data
- ✅ Google Chat alerts for new errors
- ✅ Local LLM RCA analysis being generated
- ✅ Data correlation working properly
- ✅ Local LLM models downloaded and working

---

**RCA Platform** - Intelligent Root Cause Analysis for Modern Applications 