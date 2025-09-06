#!/bin/bash

# Example Client Onboarding Script
# This demonstrates how to use the new_client_ingestion.py script

# Make the script executable and set error handling
set -e

echo "🚀 Starting Example Client Onboarding"
echo "======================================"

# Example client details
CLIENT_ID="d2-creative"
DRIVE_FOLDER_ID="1ABC123DEF456GHI789JKL"  # Replace with actual folder ID
CLIENT_URL="https://d2creative.com"

echo "👤 Client ID: $CLIENT_ID"
echo "🌐 Website: $CLIENT_URL" 
echo "💾 Drive Folder: $DRIVE_FOLDER_ID"
echo ""

# Check if required files exist
if [ ! -f "service_account.json" ]; then
    echo "❌ Error: service_account.json not found"
    echo "💡 Please ensure Google service account credentials are available"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "💡 Please create a .env file with required API keys"
    exit 1
fi

# Check if the main script exists
if [ ! -f "new_client_ingestion.py" ]; then
    echo "❌ Error: new_client_ingestion.py not found"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Run the test first
echo "🧪 Running validation tests..."
python3 test_new_client_ingestion.py

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix issues before continuing."
    exit 1
fi

echo ""
echo "✅ Tests passed. Starting client onboarding..."
echo ""

# Show the options for running the actual onboarding
echo "🚀 Ready to run client onboarding!"
echo ""
echo "Option 1 - Interactive Mode (Recommended):"
echo "python3 new_client_ingestion.py"
echo ""
echo "Option 2 - Batch Mode with the example data above:"
echo "python3 new_client_ingestion.py --batch-mode --client-id \"$CLIENT_ID\" --drive-folder-id \"$DRIVE_FOLDER_ID\" --client-homepage-url \"$CLIENT_URL\""
echo ""

# Uncomment this line when you're ready to test with real data:
# python3 new_client_ingestion.py

echo "💡 Example onboarding script completed"
echo ""
echo "To run the actual onboarding:"
echo "1. Interactive Mode: Just run 'python3 new_client_ingestion.py'"
echo "2. Batch Mode: Uncomment the batch mode line above"
echo "3. Or run manually with your own parameters"
