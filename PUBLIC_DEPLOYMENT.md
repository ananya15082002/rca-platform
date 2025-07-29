# 🚀 Public Dashboard Deployment Guide

## Overview
This guide will help you deploy the RCA Dashboard to make it accessible to everyone via a public URL.

## ✅ What's Already Done

### 1. Dashboard Redirect Links Added
- ✅ Added "Share Error Link" button to each error card
- ✅ Links use format: `https://your-domain.com/dashboard?highlight={error_id}`
- ✅ When clicked, opens dashboard and highlights the specific error card

### 2. Frontend Build Ready
- ✅ React app built and optimized
- ✅ Production build created in `frontend/build/`
- ✅ Deployment package created: `rca-dashboard-frontend.tar.gz`

## 🚀 Quick Deployment Options

### Option 1: Netlify (Recommended - Free)
1. Go to [netlify.com](https://netlify.com)
2. Drag and drop the `frontend/build` folder to the deployment area
3. Your site will be live in seconds with a URL like: `https://random-name.netlify.app`
4. Update the `DASHBOARD_BASE_URL` in your backend `.env` file

### Option 2: Vercel (Free)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `cd frontend && vercel`
3. Follow the prompts to deploy
4. Get a URL like: `https://your-project.vercel.app`

### Option 3: GitHub Pages
1. Push your code to GitHub
2. Go to repository Settings > Pages
3. Select source branch and deploy
4. Get URL like: `https://username.github.io/repo-name`

### Option 4: Firebase Hosting
1. Install Firebase CLI: `npm install -g firebase-tools`
2. Run: `firebase init hosting`
3. Deploy: `firebase deploy`

## 🔧 Configuration Updates

### 1. Update Backend Environment
After deploying, update your `.env` file:

```bash
# Update this to your deployed dashboard URL
DASHBOARD_BASE_URL=https://your-deployed-dashboard.netlify.app
```

### 2. Update Frontend API Configuration
If your backend is also deployed, update the API URL in the frontend:

```javascript
// In frontend/src/components/Dashboard.js
const API_BASE_URL = 'https://your-backend-url.com';
```

## 📋 Deployment Checklist

- [ ] Deploy frontend to a public hosting service
- [ ] Get the public dashboard URL
- [ ] Update `DASHBOARD_BASE_URL` in backend `.env`
- [ ] Test the "Share Error Link" functionality
- [ ] Verify Google Chat alerts use the public URL
- [ ] Share the dashboard URL with your team

## 🔗 Example URLs

After deployment, your URLs will look like:
- **Dashboard**: `https://rca-dashboard.netlify.app`
- **Error Link**: `https://rca-dashboard.netlify.app/dashboard?highlight=error-id`
- **Google Chat**: Will automatically use the public dashboard URL

## 🎯 Features Available

### Public Dashboard Features
- ✅ Real-time error monitoring
- ✅ Analytics charts and graphs
- ✅ Error card details with traces, spans, logs
- ✅ RCA analysis reports
- ✅ Shareable error links
- ✅ Google Chat integration

### Error Card Links
- ✅ Each error card has a "Share Error Link" button
- ✅ Links directly to the specific error with highlighting
- ✅ Works on any device/browser
- ✅ No login required

## 🚨 Important Notes

1. **Backend API**: Make sure your backend API is also publicly accessible
2. **CORS**: Configure CORS on your backend to allow requests from your frontend domain
3. **Environment Variables**: Update all environment variables for production
4. **SSL**: Use HTTPS for production deployments

## 📞 Support

If you need help with deployment:
1. Check the hosting service's documentation
2. Verify all environment variables are set correctly
3. Test the API connectivity from the deployed frontend

## 🎉 Success!

Once deployed, your RCA Dashboard will be:
- ✅ Accessible to everyone via public URL
- ✅ Shareable error links work perfectly
- ✅ Google Chat alerts link to the public dashboard
- ✅ Real-time updates every 5 minutes
- ✅ No login or authentication required 