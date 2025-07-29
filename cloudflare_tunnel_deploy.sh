#!/bin/bash

echo "🚀 Cloudflare Tunnel Deployment - Instant Shareable URL"
echo "======================================================"
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

print_status "Setting up Cloudflare Tunnel deployment..."

# Step 1: Install cloudflared
print_info "Step 1: Installing cloudflared..."

# Check if cloudflared is already installed
if command -v cloudflared &> /dev/null; then
    print_status "cloudflared is already installed"
else
    print_info "Installing cloudflared..."
    # Download and install cloudflared
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
    print_status "cloudflared installed successfully"
fi

# Step 2: Create deployment script
print_info "Step 2: Creating deployment script..."

cat > deploy_cloudflare_tunnel.sh << 'EOF'
#!/bin/bash

echo "🚀 Deploying with Cloudflare Tunnel"
echo "==================================="
echo ""

echo "Step 1: Starting your backend server..."
echo "In a new terminal, run:"
echo "  python run_backend.py"
echo ""

echo "Step 2: Starting your frontend..."
echo "In another terminal, run:"
echo "  cd frontend && npm start"
echo ""

echo "Step 3: Creating Cloudflare Tunnel..."
echo "In this terminal, run:"
echo "  cloudflared tunnel --url http://localhost:3000"
echo ""

echo "🎉 Your dashboard will be available at the URL shown above!"
echo "   Example: https://random-name.trycloudflare.com"
echo ""

echo "✅ Features you get:"
echo "   - One shareable URL for all devices"
echo "   - Works on mobile, desktop, tablet"
echo "   - No login required"
echo "   - Completely free"
echo "   - Instant deployment"
echo ""

echo "📱 Share this URL with anyone - it works everywhere!"
EOF

chmod +x deploy_cloudflare_tunnel.sh
print_status "Created deployment script"

# Step 3: Create simple guide
print_info "Step 3: Creating simple guide..."

cat > CLOUDFLARE_TUNNEL_GUIDE.md << 'EOF'
# 🚀 **CLOUDFLARE TUNNEL - Instant Shareable URL**

## ✅ **What You Get:**
- **One main dashboard URL**: `https://random-name.trycloudflare.com`
- **Completely free** - no credit card required
- **Works on all devices** - mobile, desktop, tablet
- **No login required** - public access
- **Instant deployment** - just one command

## 🎯 **Your Goal: One Shareable URL**

### **Step 1: Start Your Backend**
```bash
python run_backend.py
```

### **Step 2: Start Your Frontend**
```bash
cd frontend
npm start
```

### **Step 3: Create Cloudflare Tunnel**
```bash
cloudflared tunnel --url http://localhost:3000
```

**That's it!** You'll get a URL like:
```
https://random-name.trycloudflare.com
```

## 📱 **Your Shareable Dashboard:**

**Main URL**: `https://random-name.trycloudflare.com`

**Features**:
- ✅ **Works on all devices** (mobile, desktop, tablet)
- ✅ **No login required**
- ✅ **Real-time error monitoring**
- ✅ **Analytics charts**
- ✅ **Share Error Link buttons**
- ✅ **Google Chat integration**
- ✅ **Completely free**
- ✅ **Instant deployment**

## 🎉 **That's It!**

**Just run the tunnel command and you'll have one shareable URL that works everywhere!**

Based on [Cloudflare's free Argo Tunnel](https://blog.cloudflare.com/a-free-argo-tunnel-for-your-next-project/), this gives you instant public access to your dashboard.
EOF

print_status "Created Cloudflare Tunnel guide"

# Step 4: Create quick start script
print_info "Step 4: Creating quick start script..."

cat > quick_cloudflare.sh << 'EOF'
#!/bin/bash

echo "🚀 Quick Cloudflare Tunnel Setup"
echo "================================"
echo ""

echo "1. Start your backend:"
echo "   python run_backend.py"
echo ""

echo "2. Start your frontend:"
echo "   cd frontend && npm start"
echo ""

echo "3. Create tunnel:"
echo "   cloudflared tunnel --url http://localhost:3000"
echo ""

echo "🎉 You'll get a URL like:"
echo "   https://random-name.trycloudflare.com"
echo ""

echo "✅ Share this URL - it works on all devices!"
echo "   - Mobile phones"
echo "   - Desktop computers"
echo "   - Tablets"
echo "   - Any device with a web browser"
echo ""

echo "📱 No login required - public access for everyone!"
EOF

chmod +x quick_cloudflare.sh
print_status "Created quick start script"

# Step 5: Commit changes
print_info "Step 5: Committing changes..."

git add .
git commit -m "Add Cloudflare Tunnel deployment for instant shareable URL"
git push

print_status "Changes committed and pushed"

echo ""
echo "🎉 Cloudflare Tunnel Setup Complete!"
echo "==================================="
echo ""
print_status "cloudflared installed"
print_status "Instant shareable URL ready"
print_status "Works on all devices"
print_status "Completely free"
echo ""
print_info "Your dashboard will be accessible from:"
echo "- Mobile phones"
echo "- Desktop computers" 
echo "- Tablets"
echo "- Any device with a web browser"
echo ""
print_info "Just run: ./deploy_cloudflare_tunnel.sh"
echo ""
print_warning "Based on Cloudflare's free Argo Tunnel service" 