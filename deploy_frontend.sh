#!/bin/bash

echo "🚀 Deploying RCA Dashboard Frontend..."

# Build the frontend
cd frontend
echo "📦 Building React app..."
npm run build

# Create deployment package
echo "📁 Creating deployment package..."
cd ..
tar -czf rca-dashboard-frontend.tar.gz -C frontend/build .

echo "✅ Frontend build completed!"
echo ""
echo "📋 Deployment Instructions:"
echo "1. Upload 'rca-dashboard-frontend.tar.gz' to any static hosting service:"
echo "   - Netlify (drag & drop to netlify.com)"
echo "   - Vercel (vercel.com)"
echo "   - GitHub Pages"
echo "   - Surge.sh"
echo "   - Firebase Hosting"
echo ""
echo "2. Update the backend API URL in the deployed frontend"
echo "3. Share the public URL with your team"
echo ""
echo "🔗 Quick Deploy Options:"
echo "- Netlify: Go to netlify.com, drag the 'build' folder from frontend/"
echo "- Vercel: Install Vercel CLI and run 'vercel' in the frontend directory"
echo "- GitHub Pages: Push to GitHub and enable Pages in repository settings" 