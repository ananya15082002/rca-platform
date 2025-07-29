#!/bin/bash

echo "🚀 Deploying to GitHub Pages"
echo "============================"
echo ""

echo "Step 1: Installing gh-pages..."
cd frontend
npm install gh-pages --save-dev

echo ""
echo "Step 2: Building and deploying..."
npm run deploy

echo ""
echo "Step 3: Enable GitHub Pages"
echo "=========================="
echo "1. Go to: https://github.com/ananya15082002/rca-platform"
echo "2. Click 'Settings' tab"
echo "3. Scroll to 'Pages' section"
echo "4. Select 'Deploy from a branch'"
echo "5. Choose 'gh-pages' branch"
echo "6. Click 'Save'"
echo ""

echo "🎉 Your dashboard will be available at:"
echo "   https://ananya15082002.github.io/rca-platform"
echo ""

echo "✅ That's it! One shareable URL for all devices!"
