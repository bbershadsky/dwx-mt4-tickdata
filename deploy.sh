#!/bin/bash

# DWX Tick Data Web Server - Railway Deployment Script
# This script automates the deployment process to Railway

set -e

echo "🚀 DWX Tick Data Web Server - Railway Deployment"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}Railway CLI is not installed!${NC}"
    echo "Please install it first:"
    echo "  npm install -g @railway/cli"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
fi

# Login to Railway
echo -e "${YELLOW}Logging into Railway...${NC}"
railway login

# Initialize Railway project
echo -e "${YELLOW}Initializing Railway project...${NC}"
railway init

# Set environment variables
echo -e "${YELLOW}Setting environment variables...${NC}"
railway variables set ENVIRONMENT=production
railway variables set HOST=0.0.0.0
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

# Ask user for custom symbols
echo -e "${YELLOW}Enter your trading symbols (comma-separated) or press Enter for default:${NC}"
read -p "Symbols [EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi]: " symbols
if [ ! -z "$symbols" ]; then
    railway variables set SYMBOLS="$symbols"
fi

# Ask user for timeframes
echo -e "${YELLOW}Enter your timeframes (comma-separated) or press Enter for default:${NC}"
read -p "Timeframes [M1,M5,M15,M30,H1,H4,D1]: " timeframes
if [ ! -z "$timeframes" ]; then
    railway variables set TIMEFRAMES="$timeframes"
fi

# Deploy
echo -e "${YELLOW}Deploying to Railway...${NC}"
railway up

# Get the deployment URL
echo -e "${GREEN}Getting deployment URL...${NC}"
url=$(railway status --json | jq -r '.deployments[0].url')

echo ""
echo "🎉 Deployment successful!"
echo "================================================="
echo -e "${GREEN}Your app is now live at: $url${NC}"
echo ""
echo "📊 Next steps:"
echo "1. Open your app: $url"
echo "2. Set up your local MT4 data collector"
echo "3. Configure webhooks to send data to your cloud app"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "🔧 To update your app:"
echo "  git add ."
echo "  git commit -m \"Update app\""
echo "  railway up"
echo ""
echo "🔍 To view logs:"
echo "  railway logs"
echo ""
echo "⚙️  To manage environment variables:"
echo "  railway variables"
echo ""

# Open the deployed app
read -p "Open your deployed app in browser? (y/n): " open_app
if [[ $open_app == "y" || $open_app == "Y" ]]; then
    if command -v open &> /dev/null; then
        open "$url"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$url"
    else
        echo "Please open $url in your browser"
    fi
fi

echo -e "${GREEN}Deployment complete! 🚀${NC}" 