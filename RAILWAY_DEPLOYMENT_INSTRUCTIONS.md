# 🚀 Railway Deployment Instructions

## Quick Deploy Steps:

1. **Go to**: https://railway.app/
2. **Sign up** with GitHub
3. **Click** "New Project"
4. **Choose** "Deploy from GitHub repo"
5. **Select**: `ananya15082002/rca-platform`
6. **Railway will auto-detect** Python project

## Add PostgreSQL Database:
1. **In your Railway project**
2. **Click** "New" → "Database" → "PostgreSQL"
3. **Railway will auto-set** `DATABASE_URL`

## Set Environment Variables:
In Railway dashboard → Variables, add:

```
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAQAJSJGzQo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lrJ-5USNWwEZcG7p0e9X6uQTGYeLn60yY7SkgpTXUhQ
METRIC_URL=http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range
TRACE_BASE_URL=https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search
LOGS_API_URL=http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query
ENVIRONMENT=production
```

## Deploy Frontend:
1. **Create new service** in same Railway project
2. **Select** `frontend` directory
3. **Set build command**: `npm install && npm run build`
4. **Set start command**: `npm start`

## Your URLs will be:
- **Backend API**: `https://your-app-name.railway.app`
- **Frontend**: `https://your-frontend-name.railway.app`

## Update Dashboard URL:
After deployment, update `DASHBOARD_BASE_URL` in Railway environment variables to your frontend URL.

