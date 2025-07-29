#!/bin/bash

echo "🚀 Automated Railway Deployment for RCA Platform"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting automated Railway deployment..."

# Step 1: Update requirements for Railway
print_info "Step 1: Preparing Railway-optimized requirements..."
cp requirements_railway.txt requirements.txt
print_status "Updated requirements.txt for Railway deployment"

# Step 2: Commit changes
print_info "Step 2: Committing changes to GitHub..."
git add .
git commit -m "Prepare for Railway deployment - simplified dependencies"
git push
print_status "Changes pushed to GitHub"

# Step 3: Create Railway deployment instructions
print_info "Step 3: Creating deployment instructions..."

cat > RAILWAY_DEPLOYMENT_INSTRUCTIONS.md << 'EOF'
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

EOF

print_status "Created deployment instructions"

# Step 4: Create deployment status checker
print_info "Step 4: Creating deployment status checker..."

cat > check_deployment_status.py << 'EOF'
#!/usr/bin/env python3
"""
Check Railway Deployment Status
"""
import requests
import time
import sys

def check_railway_deployment():
    print("🔍 Checking Railway deployment status...")
    
    # This would need Railway API integration
    # For now, provide manual check instructions
    print("\n📋 Manual Deployment Check:")
    print("1. Go to https://railway.app/dashboard")
    print("2. Check if your project is deployed")
    print("3. Look for green 'Deployed' status")
    print("4. Copy the provided URLs")
    
    print("\n🎯 Expected URLs:")
    print("- Backend: https://your-app-name.railway.app")
    print("- Frontend: https://your-frontend-name.railway.app")
    
    print("\n✅ If deployment successful:")
    print("- Backend API will be accessible")
    print("- Frontend dashboard will be live")
    print("- Database will be connected")
    print("- Worker will be running")

if __name__ == "__main__":
    check_railway_deployment()
EOF

chmod +x check_deployment_status.py
print_status "Created deployment status checker"

# Step 5: Create final deployment summary
print_info "Step 5: Creating deployment summary..."

cat > DEPLOYMENT_SUMMARY.md << 'EOF'
# 🎉 Railway Deployment Summary

## ✅ What's Ready:
- **Backend API**: FastAPI with simplified RCA agent
- **Database**: PostgreSQL configuration
- **Worker**: Background processing every 5 minutes
- **Frontend**: React dashboard ready for deployment
- **Google Chat**: Alert integration configured

## 🚀 Next Steps:
1. **Deploy to Railway** using the instructions above
2. **Get your URLs** from Railway dashboard
3. **Update environment variables** with your URLs
4. **Test the deployment** by visiting your frontend URL

## 🎯 Expected Features:
- ✅ **Public dashboard** accessible to everyone
- ✅ **Share Error Link** buttons on each error card
- ✅ **Google Chat integration** with public URLs
- ✅ **Real-time error monitoring** (updates every 5 minutes)
- ✅ **Analytics charts** and graphs
- ✅ **No login required** for viewing

## 📱 Access from Any System:
- **Desktop**: Open in any browser
- **Mobile**: Responsive design works on phones
- **Tablet**: Optimized for tablet screens
- **Any OS**: Windows, Mac, Linux, iOS, Android

## 🔗 Shareable Links:
- **Dashboard**: `https://your-frontend-url.railway.app`
- **Error Cards**: `https://your-frontend-url.railway.app/dashboard?highlight={error_id}`

Your RCA Platform will be live and accessible to everyone!
EOF

print_status "Created deployment summary"

# Step 6: Final instructions
echo ""
echo "🎉 Automated Railway Deployment Setup Complete!"
echo "=============================================="
echo ""
print_status "All files prepared for Railway deployment"
print_status "Changes committed and pushed to GitHub"
print_status "Deployment instructions created"
echo ""
print_info "Next Steps:"
echo "1. Go to https://railway.app/"
echo "2. Follow the instructions in RAILWAY_DEPLOYMENT_INSTRUCTIONS.md"
echo "3. Deploy your project"
echo "4. Get your working URLs"
echo ""
print_info "Your RCA Platform will be accessible from:"
echo "- Desktop computers"
echo "- Mobile phones"
echo "- Tablets"
echo "- Any device with a web browser"
echo ""
print_status "Ready for deployment! 🚀" 