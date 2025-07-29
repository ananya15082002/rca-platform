# RCA Platform - Root Cause Analysis Platform

A comprehensive cloud-hosted platform that continuously ingests error metrics, traces, and logs from CubeAPM and Coralogix; analyzes & correlates incidents; performs RCA (Root Cause Analysis) using local LLMs; and provides a beautiful live dashboard with Google Chat integration for team alerts.

## 🚀 Features

- **Continuous Monitoring**: Runs every 5 minutes to fetch error metrics
- **Data Correlation**: Correlates error cards with traces, spans, and logs
- **Local LLM-Powered RCA**: Uses local models for intelligent root cause analysis (no API limits!)
- **Real-time Alerts**: Google Chat integration for instant notifications
- **Beautiful Dashboard**: Modern React frontend with charts and detailed views
- **Public Access**: Shareable links, no login required
- **Data Export**: Download complete correlation data as JSON

## 📁 Project Structure

```
RCA_Agent_5xx_Error/
├── app/                    # Backend FastAPI application
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── ingestion.py       # Data ingestion logic
│   ├── rca_agent.py       # Local LLM RCA agent
│   ├── google_chat.py     # Google Chat integration
│   ├── worker.py          # Background worker
│   └── main.py           # FastAPI app with REST endpoints
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js        # Main app component
│   │   └── index.js      # Entry point
│   ├── package.json      # Frontend dependencies
│   └── tailwind.config.js # Tailwind CSS config
├── requirements.txt       # Python dependencies
├── run_backend.py        # Backend startup script
├── run_worker.py         # Worker startup script
└── README.md            # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- **No API keys needed!** Uses local LLM models

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
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

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Environment Configuration

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/rca_platform

# Local LLM Configuration (No API key needed!)
# The system will automatically download and use a local model
# Available models: microsoft/DialoGPT-medium, gpt2, EleutherAI/gpt-neo-125M

# Google Chat Webhook
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAQAJSJGzQo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lrJ-5USNWwEZcG7p0e9X6uQTGYeLn60yY7SkgpTXUhQ

# CubeAPM Configuration
METRIC_URL=http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range
TRACE_BASE_URL=https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search
LOGS_API_URL=http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query

# Application Settings
ENVIRONMENT=production
DASHBOARD_BASE_URL=https://your-deployment-url.com
```

## 🚀 Running the Application

### Development Mode

1. **Start the Backend API**:
```bash
python run_backend.py
```

2. **Start the Background Worker** (in a separate terminal):
```bash
python run_worker.py
```

3. **Start the Frontend** (in another terminal):
```bash
cd frontend
npm start
```

### Production Deployment

The application can be deployed on various platforms:

- **Render.com**: Use the provided `render.yaml`
- **Railway.app**: Direct deployment from GitHub
- **Fly.io**: Use `fly.toml` configuration
- **Vercel**: Frontend deployment
- **Heroku**: Backend deployment

## 📊 API Endpoints

### Core Endpoints

- `GET /` - Health check
- `GET /api/health` - API health status
- `GET /api/errors` - List error metrics
- `GET /api/errors/{error_id}` - Get error details
- `GET /api/errors/{error_id}/download` - Download correlation data
- `GET /api/stats` - Platform statistics
- `POST /api/trigger-cycle` - Manually trigger ingestion cycle

### Query Parameters

- `hours` - Time window (default: 24)
- `env` - Filter by environment
- `service` - Filter by service

## 🎯 Dashboard Features

### Main Dashboard
- **Real-time Statistics**: Error counts, traces, logs, RCA reports
- **Interactive Charts**: Environment and service breakdowns
- **Error Cards**: Clickable error summaries with quick actions
- **Live Updates**: Auto-refresh every 5 minutes
- **Filtering**: By environment, service, and time window

### Error Detail View
- **Overview Tab**: Summary statistics and RCA analysis
- **Traces Tab**: All trace IDs for the error
- **Spans Tab**: Detailed span information in table format
- **Logs Tab**: All related logs with JSON formatting
- **RCA Analysis Tab**: Local LLM-generated root cause analysis
- **Download**: Complete correlation data as JSON

## 🔧 Background Worker

The worker runs continuously and:

1. **Fetches Error Metrics**: Every 5 minutes from CubeAPM
2. **Correlates Data**: Links errors with traces and logs
3. **Generates RCA**: Uses local LLM for analysis (no API limits!)
4. **Sends Alerts**: Google Chat notifications for new errors
5. **Stores Data**: Saves everything to PostgreSQL

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

## 📱 Google Chat Integration

When a new error is detected, the system automatically sends a structured alert card to Google Chat containing:

- Environment and service information
- Error details (HTTP code, exception, count)
- Time window
- Local LLM-generated RCA summary preview
- Direct link to dashboard

## 🗄️ Database Schema

### Tables

- **error_metrics**: Error card data with timestamps
- **traces**: Trace IDs linked to error metrics
- **spans**: Span metadata with operations and timing
- **logs**: Log data grouped by trace ID
- **rca_reports**: Local LLM analysis results

### Indexes

- Time-based indexes for efficient queries
- Error metric ID indexes for joins
- Trace ID indexes for correlation

## 🔍 Data Flow

1. **Ingestion**: Worker fetches error metrics every 5 minutes
2. **Correlation**: For each error, fetch related traces and logs
3. **Analysis**: Local LLM analyzes the complete correlation bundle
4. **Storage**: All data saved to PostgreSQL with proper indexing
5. **Alerting**: Google Chat notification sent for new errors
6. **Dashboard**: Real-time display with filtering and drill-down

## 🎨 Frontend Technologies

- **React 18**: Modern component-based UI
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Interactive data visualization
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing

## 🔒 Security & Configuration

- **Environment Variables**: All secrets configurable via `.env`
- **CORS**: Configured for cross-origin requests
- **Database**: PostgreSQL with proper indexing
- **Local LLM**: No external API dependencies
- **Public Access**: No authentication required for dashboard

## 📈 Monitoring & Observability

- **Health Checks**: API endpoint for monitoring
- **Error Logging**: Comprehensive error handling
- **Performance**: Optimized database queries
- **Real-time Updates**: Live dashboard with auto-refresh
- **Data Export**: Complete correlation data download

## 🚀 Deployment Instructions

### Quick Deploy (Render.com)

1. **Fork** this repository to your GitHub account
2. **Connect** to Render.com
3. **Create** new Web Service from GitHub
4. **Configure** environment variables in Render dashboard
5. **Deploy** automatically

**Required Environment Variables:**
- `DATABASE_URL` (PostgreSQL connection string)
- `GOOGLE_CHAT_WEBHOOK_URL` (Already configured)
- `METRIC_URL`, `TRACE_BASE_URL`, `LOGS_API_URL` (Already configured)

### Manual Deployment

1. **Backend**: Deploy FastAPI app to your preferred platform
2. **Database**: Set up PostgreSQL instance
3. **Frontend**: Build and deploy React app
4. **Worker**: Run background worker process
5. **Environment**: Configure all environment variables

## 📞 Support

For issues or questions:

1. Check the logs for error details
2. Verify environment variable configuration
3. Test API endpoints directly
4. Review database connectivity

## 🔄 Development

### Adding New Features

1. **Backend**: Add new endpoints in `app/main.py`
2. **Models**: Update database schema in `app/models.py`
3. **Frontend**: Create new components in `frontend/src/components/`
4. **Worker**: Extend ingestion logic in `app/worker.py`

### Testing

```bash
# Backend tests
python -m pytest

# Frontend tests
cd frontend && npm test
```

## 📄 License

This project is open source and available under the MIT License.

---

**RCA Platform** - Intelligent Root Cause Analysis for Modern Applications 