#!/bin/bash

echo "🔧 Environment Configuration After Deployment"
echo "==========================================="
echo ""

echo "After you deploy to Netlify and get your public URL, run this script:"
echo ""
echo "1. Replace YOUR_DEPLOYED_URL with your actual Netlify URL"
echo "2. Update your backend .env file"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "📝 Current .env file found. You can update it with:"
    echo ""
    echo "   DASHBOARD_BASE_URL=https://your-deployed-url.netlify.app"
    echo ""
    echo "Example:"
    echo "   DASHBOARD_BASE_URL=https://rca-dashboard-123.netlify.app"
    echo ""
else
    echo "📝 Create a .env file with:"
    echo ""
    echo "DATABASE_URL=postgresql://username:password@localhost:5432/rca_platform"
    echo "GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/AAQAJSJGzQo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lrJ-5USNWwEZcG7p0e9X6uQTGYeLn60yY7SkgpTXUhQ"
    echo "METRIC_URL=http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range"
    echo "TRACE_BASE_URL=https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search"
    echo "LOGS_API_URL=http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query"
    echo "ENVIRONMENT=production"
    echo "DASHBOARD_BASE_URL=https://your-deployed-url.netlify.app"
    echo ""
fi

echo "🎯 What happens after deployment:"
echo "   ✅ Dashboard will be accessible to everyone"
echo "   ✅ Share Error Link buttons will work"
echo "   ✅ Google Chat alerts will use the public URL"
echo "   ✅ No login required for viewing"
echo "   ✅ Works on all devices and browsers"
echo ""

echo "🚀 Ready to deploy! Follow the Netlify steps above." 