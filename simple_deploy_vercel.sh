#!/bin/bash

echo "🚀 Simple Vercel Deployment - One Shareable Dashboard URL"
echo "========================================================"
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

print_status "Creating simple Vercel deployment..."

# Step 1: Create Vercel configuration
print_info "Step 1: Creating Vercel configuration..."

cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-backend-url.railway.app"
  }
}
EOF

print_status "Created vercel.json"

# Step 2: Update frontend for production
print_info "Step 2: Updating frontend for production..."

cat > frontend/.env.production << 'EOF'
REACT_APP_API_URL=https://your-backend-url.railway.app
EOF

print_status "Created production environment file"

# Step 3: Create deployment instructions
print_info "Step 3: Creating deployment instructions..."

cat > SIMPLE_DEPLOYMENT_GUIDE.md << 'EOF'
# 🚀 **SIMPLE DEPLOYMENT - One Shareable Dashboard URL**

## ✅ **What You Get:**
- **One main dashboard URL** that works on all devices
- **No complex setup** - just deploy and get URL
- **Works on mobile, desktop, tablet** - any device
- **No login required** - public access

## 🎯 **Your Goal: One Shareable URL**

### **Option 1: Vercel (Recommended - Fastest)**

1. **Go to**: https://vercel.com/
2. **Sign up** with GitHub
3. **Click** "New Project"
4. **Import** your GitHub repo: `ananya15082002/rca-platform`
5. **Set Root Directory**: `frontend`
6. **Set Build Command**: `npm run build`
7. **Set Output Directory**: `build`
8. **Click** "Deploy"

**Your URL will be**: `https://your-project-name.vercel.app`

### **Option 2: Netlify (Also Easy)**

1. **Go to**: https://netlify.com/
2. **Click** "Add new site" → "Import an existing project"
3. **Connect** to GitHub
4. **Select** repo: `ananya15082002/rca-platform`
5. **Set Base directory**: `frontend`
6. **Set Build command**: `npm run build`
7. **Set Publish directory**: `build`
8. **Click** "Deploy site"

**Your URL will be**: `https://your-site-name.netlify.app`

## 🔧 **After Deployment:**

1. **Get your frontend URL** (from Vercel/Netlify)
2. **Update backend** to use your frontend URL:
   ```bash
   DASHBOARD_BASE_URL=https://your-frontend-url.vercel.app
   ```

## 📱 **Your Shareable Dashboard:**

**Main URL**: `https://your-frontend-url.vercel.app`

**Features**:
- ✅ **Works on all devices** (mobile, desktop, tablet)
- ✅ **No login required**
- ✅ **Real-time error monitoring**
- ✅ **Analytics charts**
- ✅ **Share Error Link buttons**
- ✅ **Google Chat integration**

## 🎉 **That's It!**

**Just deploy and you'll have one shareable URL that works everywhere!**
EOF

print_status "Created simple deployment guide"

# Step 4: Create quick deploy script
print_info "Step 4: Creating quick deploy script..."

cat > quick_deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Quick Deploy Options"
echo "======================="
echo ""

echo "Choose your deployment method:"
echo ""
echo "1. Vercel (Recommended - Fastest)"
echo "   - Go to https://vercel.com/"
echo "   - Import GitHub repo: ananya15082002/rca-platform"
echo "   - Set Root Directory: frontend"
echo "   - Deploy and get URL"
echo ""

echo "2. Netlify (Also Easy)"
echo "   - Go to https://netlify.com/"
echo "   - Import GitHub repo: ananya15082002/rca-platform"
echo "   - Set Base directory: frontend"
echo "   - Deploy and get URL"
echo ""

echo "🎯 Your Goal: One Shareable URL"
echo "   - Works on mobile, desktop, tablet"
echo "   - No login required"
echo "   - Public access for everyone"
echo ""

echo "📱 After deployment, your URL will be:"
echo "   https://your-project-name.vercel.app"
echo "   or"
echo "   https://your-site-name.netlify.app"
echo ""

echo "✅ Ready to deploy! Choose Vercel or Netlify above."
EOF

chmod +x quick_deploy.sh
print_status "Created quick deploy script"

# Step 5: Commit changes
print_info "Step 5: Committing changes..."

git add .
git commit -m "Add simple deployment options for one shareable URL"
git push

print_status "Changes committed and pushed"

echo ""
echo "🎉 Simple Deployment Setup Complete!"
echo "=================================="
echo ""
print_status "Ready for simple deployment"
print_status "Choose Vercel or Netlify"
print_status "Get one shareable dashboard URL"
echo ""
print_info "Your dashboard will be accessible from:"
echo "- Mobile phones"
echo "- Desktop computers" 
echo "- Tablets"
echo "- Any device with a web browser"
echo ""
print_info "Just deploy and get your URL!"
echo ""
print_warning "Run: ./quick_deploy.sh for instructions" 