#!/bin/bash

echo "🚀 RCA Dashboard Quick Deployment"
echo "=================================="
echo ""

# Check if build exists
if [ ! -d "frontend/build" ]; then
    echo "❌ Build directory not found. Building frontend..."
    cd frontend
    npm run build
    cd ..
fi

echo "✅ Frontend build ready!"
echo ""

echo "📋 Choose your deployment method:"
echo ""
echo "1. Netlify (Recommended - Free, No CLI needed)"
echo "   - Go to https://netlify.com"
echo "   - Drag and drop the 'frontend/build' folder"
echo "   - Get URL like: https://random-name.netlify.app"
echo ""
echo "2. Vercel (Free, CLI required)"
echo "   - Run: npm install -g vercel"
echo "   - Run: cd frontend && vercel"
echo ""
echo "3. GitHub Pages (Free)"
echo "   - Push code to GitHub"
echo "   - Enable Pages in repository settings"
echo ""
echo "4. Firebase Hosting (Free)"
echo "   - Run: npm install -g firebase-tools"
echo "   - Run: firebase init hosting"
echo "   - Run: firebase deploy"
echo ""

echo "🔧 After deployment, update your backend .env file:"
echo "   DASHBOARD_BASE_URL=https://your-deployed-url.com"
echo ""

echo "📁 Your build files are in: frontend/build/"
echo "📦 Deployment package: rca-dashboard-frontend.tar.gz"
echo ""

echo "🎯 Features ready for deployment:"
echo "   ✅ Share Error Link buttons on each error card"
echo "   ✅ Public dashboard accessible to everyone"
echo "   ✅ Google Chat integration with public URLs"
echo "   ✅ Real-time error monitoring"
echo "   ✅ Analytics charts and graphs"
echo ""

echo "🚀 Ready to deploy! Choose your method above." 