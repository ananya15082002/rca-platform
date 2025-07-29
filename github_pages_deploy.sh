#!/bin/bash

echo "🚀 GitHub Pages Deployment - Simplest Option"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_status "Setting up GitHub Pages deployment..."

# Step 1: Create GitHub Pages configuration
print_info "Step 1: Creating GitHub Pages configuration..."

cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
        
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
        
    - name: Build
      run: |
        cd frontend
        npm run build
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend/build
EOF

print_status "Created GitHub Pages workflow"

# Step 2: Update package.json for GitHub Pages
print_info "Step 2: Updating package.json for GitHub Pages..."

cat > frontend/package.json << 'EOF'
{
  "name": "rca-dashboard",
  "version": "0.1.0",
  "private": true,
  "homepage": "https://ananya15082002.github.io/rca-platform",
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.4",
    "@testing-library/react": "^13.3.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.263.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.1",
    "react-scripts": "5.0.1",
    "recharts": "^2.8.0",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "gh-pages": "^6.0.0"
  },
  "proxy": "http://localhost:8000"
}
EOF

print_status "Updated package.json"

# Step 3: Create simple deployment guide
print_info "Step 3: Creating simple deployment guide..."

cat > SIMPLEST_DEPLOYMENT.md << 'EOF'
# 🚀 **SIMPLEST DEPLOYMENT - One Shareable URL**

## ✅ **What You Get:**
- **One main dashboard URL**: `https://ananya15082002.github.io/rca-platform`
- **Completely free** - no credit card required
- **Works on all devices** - mobile, desktop, tablet
- **No login required** - public access
- **Automatic deployment** from GitHub

## 🎯 **Your Goal: One Shareable URL**

### **Step 1: Enable GitHub Pages**

1. **Go to**: https://github.com/ananya15082002/rca-platform
2. **Click** "Settings" tab
3. **Scroll down** to "Pages" section
4. **Under "Source"**, select "Deploy from a branch"
5. **Select branch**: `gh-pages`
6. **Click** "Save"

### **Step 2: Deploy**

1. **In your terminal**, run:
   ```bash
   cd frontend
   npm install gh-pages --save-dev
   npm run deploy
   ```

2. **Or just push to GitHub** - it will auto-deploy!

### **Step 3: Get Your URL**

**Your dashboard will be available at:**
```
https://ananya15082002.github.io/rca-platform
```

## 📱 **Your Shareable Dashboard:**

**Main URL**: `https://ananya15082002.github.io/rca-platform`

**Features**:
- ✅ **Works on all devices** (mobile, desktop, tablet)
- ✅ **No login required**
- ✅ **Real-time error monitoring**
- ✅ **Analytics charts**
- ✅ **Share Error Link buttons**
- ✅ **Google Chat integration**
- ✅ **Completely free**

## 🎉 **That's It!**

**Just enable GitHub Pages and you'll have one shareable URL that works everywhere!**

**Your URL**: `https://ananya15082002.github.io/rca-platform`
EOF

print_status "Created simplest deployment guide"

# Step 4: Create deploy script
print_info "Step 4: Creating deploy script..."

cat > deploy_github_pages.sh << 'EOF'
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
EOF

chmod +x deploy_github_pages.sh
print_status "Created deploy script"

# Step 5: Commit changes
print_info "Step 5: Committing changes..."

git add .
git commit -m "Add GitHub Pages deployment for simplest option"
git push

print_status "Changes committed and pushed"

echo ""
echo "🎉 Simplest Deployment Setup Complete!"
echo "====================================="
echo ""
print_status "GitHub Pages deployment ready"
print_status "One shareable URL for all devices"
print_status "Completely free - no credit card needed"
echo ""
print_info "Your dashboard will be at:"
echo "https://ananya15082002.github.io/rca-platform"
echo ""
print_info "Just run: ./deploy_github_pages.sh"
echo ""
print_warning "Then enable GitHub Pages in repository settings" 