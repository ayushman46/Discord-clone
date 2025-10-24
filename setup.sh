#!/bin/bash

# Discord Clone - Local Development Setup Script

set -e

echo "================================================"
echo "Discord Clone - Development Setup"
echo "================================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not in PATH (it may still be installed)"
else
    echo "✅ PostgreSQL found"
fi

# Backend Setup
echo -e "\n${YELLOW}Setting up Backend...${NC}"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please configure .env with your database credentials"
else
    echo "✅ .env file exists"
fi

cd ..

# Frontend Setup
echo -e "\n${YELLOW}Setting up Frontend...${NC}"

cd frontend

# Install Node dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install --quiet
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ Frontend .env created"
else
    echo "✅ .env file exists"
fi

cd ..

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Configure backend/.env with your PostgreSQL connection"
echo "2. Start PostgreSQL service (if not already running)"
echo "3. In one terminal, run: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "4. In another terminal, run: cd frontend && npm run dev"
echo "5. Open http://localhost:5173 in your browser"

echo -e "\n${YELLOW}Database Setup:${NC}"
echo "macOS:"
echo "  brew services start postgresql"
echo "  createdb discord_clone"
echo ""
echo "Linux:"
echo "  sudo systemctl start postgresql"
echo "  createdb discord_clone"

echo -e "\n${YELLOW}Useful commands:${NC}"
echo "Backend:"
echo "  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  # API docs: http://localhost:8000/docs"
echo ""
echo "Frontend:"
echo "  cd frontend && npm run dev"
echo "  # Frontend: http://localhost:5173"
echo ""
echo "Testing:"
echo "  # In backend directory:"
echo "  python setup_db.py  # Initialize database"
