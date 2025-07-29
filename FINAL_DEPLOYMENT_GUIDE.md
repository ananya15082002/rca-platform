# 🚀 **FINAL DEPLOYMENT GUIDE - Get Working URLs**

## ✅ **Everything is Ready!**

Your RCA Platform has been prepared for Railway deployment with:
- ✅ **Simplified dependencies** (no heavy LLM packages)
- ✅ **Railway configuration** files
- ✅ **GitHub repository** updated
- ✅ **All code** committed and pushed

## 🎯 **Your Goal: Get Working URLs Accessible from All Systems**

### **Step 1: Deploy to Railway**

1. **Go to**: https://railway.app/
2. **Sign up** with GitHub (if not already signed up)
3. **Click** "New Project"
4. **Choose** "Deploy from GitHub repo"
5. **Select**: `ananya15082002/rca-platform`
6. **Click** "Deploy"

### **Step 2: Add PostgreSQL Database**

1. **In your Railway project dashboard**
2. **Click** "New" → "Database" → "PostgreSQL"
3. **Railway will automatically**:
   - Create PostgreSQL database
   - Set `DATABASE_URL` environment variable
   - Link database to your service

### **Step 3: Set Environment Variables**

In Railway dashboard → **Variables**, add these:

```bash
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAQAJSJGzQo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lrJ-5USNWwEZcG7p0e9X6uQTGYeLn60yY7SkgpTXUhQ
METRIC_URL=http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range
TRACE_BASE_URL=https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search
LOGS_API_URL=http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query
ENVIRONMENT=production
```

### **Step 4: Deploy Frontend**

1. **In same Railway project**
2. **Click** "New Service"
3. **Choose** "GitHub Repo"
4. **Select** same repo: `ananya15082002/rca-platform`
5. **Set Base Directory**: `frontend`
6. **Set Build Command**: `npm install && npm run build`
7. **Set Start Command**: `npm start`

### **Step 5: Get Your Working URLs**

After deployment, Railway will provide:
- **Backend URL**: `https://your-app-name.railway.app`
- **Frontend URL**: `https://your-frontend-name.railway.app`

### **Step 6: Update Dashboard URL**

1. **Go back** to your Railway project
2. **Click** on your backend service
3. **Go to** "Variables"
4. **Add**: `DASHBOARD_BASE_URL=https://your-frontend-name.railway.app`

## 🎉 **Your Working URLs Will Be:**

### **Main Dashboard**
```
https://your-frontend-name.railway.app
```

### **Shareable Error Links**
```
https://your-frontend-name.railway.app/dashboard?highlight={error_id}
```

## 📱 **Accessible From:**

- ✅ **Desktop computers** (Windows, Mac, Linux)
- ✅ **Mobile phones** (iOS, Android)
- ✅ **Tablets** (iPad, Android tablets)
- ✅ **Any device** with a web browser
- ✅ **No login required**
- ✅ **Works on all systems**

## 🔗 **Features You'll Get:**

- ✅ **Public dashboard** accessible to everyone
- ✅ **Share Error Link** buttons on each error card
- ✅ **Google Chat integration** with public URLs
- ✅ **Real-time error monitoring** (updates every 5 minutes)
- ✅ **Analytics charts** and graphs
- ✅ **Responsive design** for all screen sizes

## 🚀 **Ready to Deploy!**

**Just follow the steps above and you'll have working URLs that work on all systems!**

Your RCA Platform will be live and accessible to everyone from any device! 🎯 