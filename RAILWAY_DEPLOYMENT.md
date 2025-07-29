# 🚀 Railway Deployment Guide

## Step 1: Create Railway Account
1. **Go to**: https://railway.app/
2. **Sign up** with GitHub
3. **Connect** your GitHub account

## Step 2: Deploy Backend to Railway

### Option A: Deploy from GitHub
1. **Click** "New Project"
2. **Choose** "Deploy from GitHub repo"
3. **Select** `ananya15082002/rca-platform`
4. **Railway will automatically detect** it's a Python project
5. **Set environment variables** (see below)
6. **Click** "Deploy"

### Option B: Deploy from CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Step 3: Configure Environment Variables

In Railway dashboard, go to your project → Variables and add:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# Google Chat Webhook
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAQAJSJGzQo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lrJ-5USNWwEZcG7p0e9X6uQTGYeLn60yY7SkgpTXUhQ

# CubeAPM Configuration
METRIC_URL=http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range
TRACE_BASE_URL=https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search
LOGS_API_URL=http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query

# Application Settings
ENVIRONMENT=production

# Dashboard URL (update after frontend deployment)
DASHBOARD_BASE_URL=https://your-frontend-url.com
```

## Step 4: Add PostgreSQL Database

1. **Go to** your Railway project
2. **Click** "New" → "Database" → "PostgreSQL"
3. **Railway will automatically**:
   - Create PostgreSQL database
   - Set `DATABASE_URL` environment variable
   - Link database to your service

## Step 5: Deploy Frontend

### Option A: Deploy Frontend to Railway
1. **Create new service** in same project
2. **Select** `frontend` directory
3. **Set build command**: `npm install && npm run build`
4. **Set start command**: `npm start` (or use static hosting)

### Option B: Deploy Frontend to Netlify/Vercel
1. **Deploy frontend** to Netlify/Vercel
2. **Get frontend URL**
3. **Update** `DASHBOARD_BASE_URL` in Railway environment variables

## Step 6: Configure Domains

### Backend API
- Railway provides: `https://your-app-name.railway.app`
- Custom domain: Add in Railway dashboard

### Frontend
- If using Railway: `https://your-frontend-name.railway.app`
- If using Netlify: `https://your-app.netlify.app`

## Step 7: Update Environment Variables

After getting your URLs, update in Railway:

```bash
# Backend URL (Railway provides this)
BACKEND_URL=https://your-app-name.railway.app

# Frontend URL (your deployed frontend)
DASHBOARD_BASE_URL=https://your-frontend-url.com
```

## 🎯 What You Get

- ✅ **Backend API** running on Railway
- ✅ **PostgreSQL database** managed by Railway
- ✅ **Automatic deployments** from GitHub
- ✅ **SSL certificates** included
- ✅ **Custom domains** support
- ✅ **Environment variables** management
- ✅ **Logs and monitoring** built-in

## 📋 Railway Advantages

- **Free tier** available
- **Automatic scaling**
- **Built-in PostgreSQL**
- **GitHub integration**
- **Custom domains**
- **SSL certificates**
- **Global CDN**

## 🚀 Ready to Deploy!

1. **Go to** https://railway.app/
2. **Create new project**
3. **Connect your GitHub repo**
4. **Add PostgreSQL database**
5. **Set environment variables**
6. **Deploy!**

Your RCA Platform will be live and accessible to everyone! 