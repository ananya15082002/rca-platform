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
