#!/bin/bash

echo "🚀 Deploying RCA Dashboard to Netlify"
echo "======================================"
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

echo "📋 Netlify Deployment Steps:"
echo ""
echo "1. Go to https://netlify.com"
echo "2. Click 'Add new site' → 'Deploy manually'"
echo "3. Drag and drop the 'frontend/build' folder"
echo "4. Wait for deployment (usually 30-60 seconds)"
echo "5. Get your public URL (e.g., https://random-name.netlify.app)"
echo ""

echo "📁 Your build files are ready in: frontend/build/"
echo ""

echo "🔧 After deployment, update your backend .env file:"
echo "   DASHBOARD_BASE_URL=https://your-deployed-url.netlify.app"
echo ""

echo "🎯 Features ready for deployment:"
echo "   ✅ Share Error Link buttons on each error card"
echo "   ✅ Public dashboard accessible to everyone"
echo "   ✅ Google Chat integration with public URLs"
echo "   ✅ Real-time error monitoring"
echo "   ✅ Analytics charts and graphs"
echo ""

echo "🚀 Ready to deploy! Follow the steps above."
echo ""
echo "💡 Pro tip: You can also drag the entire 'frontend/build' folder"
echo "   directly to https://app.netlify.com/drop" 