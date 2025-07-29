# 🚀 GitHub to Netlify Deployment Guide

## Step 1: Create GitHub Repository

1. **Go to**: https://github.com/new
2. **Repository name**: `rca-platform`
3. **Description**: `Root Cause Analysis Platform with FastAPI backend and React frontend`
4. **Visibility**: Public
5. **Don't initialize** with README (we already have one)
6. **Click**: "Create repository"

## Step 2: Push Code to GitHub

After creating the repository, run these commands:

```bash
git remote add origin https://github.com/ananya15082002/rca-platform.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Netlify

1. **Go to**: https://app.netlify.com/
2. **Click**: "Add new site"
3. **Choose**: "Import an existing project"
4. **Connect to Git**: Click "GitHub"
5. **Select repository**: `ananya15082002/rca-platform`
6. **Configure build settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `build`
7. **Click**: "Deploy site"

## Step 4: Configure Environment Variables

After deployment, go to your Netlify site settings:

1. **Site settings** → **Environment variables**
2. **Add variable**:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.com`

## Step 5: Update Backend Configuration

Update your backend `.env` file:

```bash
DASHBOARD_BASE_URL=https://your-netlify-site.netlify.app
```

## 🎯 What You Get

- ✅ **Automatic deployments** from GitHub
- ✅ **Public dashboard** accessible to everyone
- ✅ **Share Error Link** buttons on each error card
- ✅ **Google Chat integration** with public URLs
- ✅ **Real-time updates** every 5 minutes
- ✅ **Analytics charts** and graphs
- ✅ **No login required** for viewing

## 🔄 Continuous Deployment

Every time you push to GitHub:
1. Netlify automatically detects changes
2. Builds the frontend
3. Deploys to your public URL
4. Updates are live in minutes

## 📁 Repository Structure

```
rca-platform/
├── app/                    # FastAPI backend
│   ├── main.py            # API endpoints
│   ├── models.py          # Database models
│   ├── worker.py          # Background worker
│   ├── rca_agent.py       # LLM integration
│   └── google_chat.py     # Alert system
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # Dashboard components
│   │   └── App.js         # Main app
│   └── package.json       # Dependencies
├── requirements.txt        # Python dependencies
├── netlify.toml          # Netlify configuration
└── README.md             # Documentation
```

## 🚀 Ready to Deploy!

Follow the steps above and your RCA Platform will be live and accessible to everyone! 