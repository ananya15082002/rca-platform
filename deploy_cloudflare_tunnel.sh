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
