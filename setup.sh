#!/bin/bash

# YouTube SEO Analyzer - Setup Script

echo "=========================================="
echo "YouTube SEO Analyzer - Setup"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "✓ Python version: $(python3 --version)"
echo ""

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Setup environment file
echo ""
if [ ! -f .env ]; then
    echo "Setting up environment variables..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - YOUTUBE_API_KEY"
    echo "   - OPENAI_API_KEY (optional)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run: python youseo.py https://www.youtube.com/watch?v=VIDEO_ID"
echo ""
echo "For help: python youseo.py --help"
echo ""
