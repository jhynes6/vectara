#!/bin/bash
# Setup script for inbox_manager

echo "🔧 Setting up inbox_manager virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source inbox_manager/venv/bin/activate"
echo ""
echo "To run the app:"
echo "  cd inbox_manager && ./run.sh"

