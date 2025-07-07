#!/bin/bash

# DWX Tick Data Web Server - Render Deployment Script
# This script prepares your project for Render deployment

set -e

echo "🚀 DWX Tick Data Web Server - Render Deployment Setup"
echo "====================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed!${NC}"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
else
    echo -e "${GREEN}Git repository already exists${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore file...${NC}"
    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
.venv
venv/
.pytest_cache
.coverage
*.log
*.tmp
.DS_Store
.vscode/
.idea/
*~
*.swp
*.swo
EOF
    git add .gitignore
    git commit -m "Add .gitignore"
fi

# Check if render.yaml exists and is correct
if [ ! -f "render.yaml" ]; then
    echo -e "${YELLOW}Creating render.yaml configuration...${NC}"
    # render.yaml is already created by the assistant
    git add render.yaml
    git commit -m "Add render.yaml configuration"
else
    echo -e "${GREEN}render.yaml already exists${NC}"
fi

# Ask user for their trading symbols
echo -e "${BLUE}Customizing configuration...${NC}"
echo "Enter your trading symbols (comma-separated) or press Enter for default:"
read -p "Symbols [EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi]: " symbols
if [ ! -z "$symbols" ]; then
    # Update render.yaml with custom symbols
    sed -i.bak "s/EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi/$symbols/g" render.yaml
    rm render.yaml.bak
    git add render.yaml
    git commit -m "Update symbols in render.yaml"
fi

# Ask user for timeframes
echo "Enter your timeframes (comma-separated) or press Enter for default:"
read -p "Timeframes [M1,M5,M15,M30,H1,H4,D1]: " timeframes
if [ ! -z "$timeframes" ]; then
    # Update render.yaml with custom timeframes
    sed -i.bak "s/M1,M5,M15,M30,H1,H4,D1/$timeframes/g" render.yaml
    rm render.yaml.bak
    git add render.yaml
    git commit -m "Update timeframes in render.yaml"
fi

# Ensure all files are committed
git add .
if ! git diff --cached --quiet; then
    git commit -m "Final updates for Render deployment"
fi

echo ""
echo "✅ Your project is now ready for Render deployment!"
echo "====================================================="
echo ""
echo -e "${GREEN}🎯 Next Steps:${NC}"
echo ""
echo "1. 📂 Create a GitHub repository:"
echo "   • Go to https://github.com/new"
echo "   • Create a new repository (e.g., 'dwx-web-server')"
echo "   • Don't initialize with README, .gitignore, or license"
echo ""
echo "2. 🔗 Connect your local repository to GitHub:"
echo "   git remote add origin https://github.com/yourusername/dwx-web-server.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 🚀 Deploy to Render:"
echo "   • Go to https://render.com"
echo "   • Sign up/login with your GitHub account"
echo "   • Click 'New +' → 'Web Service'"
echo "   • Select your GitHub repository"
echo "   • Render will automatically use your render.yaml configuration!"
echo ""
echo "4. 🌐 Access your app:"
echo "   • Your app will be available at: https://your-app-name.onrender.com"
echo "   • The first deployment takes 2-3 minutes"
echo ""
echo -e "${YELLOW}💡 Pro Tips:${NC}"
echo "• Your app will sleep after 15 minutes of inactivity (free tier)"
echo "• First request after sleep takes ~30 seconds to wake up"
echo "• Use render.yaml for infrastructure as code"
echo "• Monitor your app at https://dashboard.render.com"
echo ""
echo -e "${GREEN}📖 Read the full guide: RENDER_DEPLOYMENT.md${NC}"
echo ""
echo -e "${BLUE}🔧 For local MT4 data forwarding:${NC}"
echo "• See 'Connecting Your Local MT4 to Cloud' section in the guide"
echo "• Your MT4 system will need to send data to your Render app"
echo ""

# Ask if user wants to open GitHub
read -p "Open GitHub to create a new repository? (y/n): " open_github
if [[ $open_github == "y" || $open_github == "Y" ]]; then
    if command -v open &> /dev/null; then
        open "https://github.com/new"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/new"
    else
        echo "Please open https://github.com/new in your browser"
    fi
fi

echo ""
echo -e "${GREEN}🎉 Happy Trading! Your tick data dashboard will be live soon! 📊${NC}" 