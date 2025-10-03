#!/bin/bash
# Quick setup script for Vertex AI RAG

set -e

echo "🚀 Vertex AI RAG - Quick Setup"
echo "=" | tr -d '\n' | head -c 80 | tr '\0' '='
echo ""

cd vertex_ai_rag

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env from template..."
    cp .env.template .env
    echo "⚠️  IMPORTANT: Edit .env file with your credentials before continuing"
    echo "   Required: GOOGLE_CLOUD_PROJECT, OPENAI_API_KEY, GOOGLE_SEARCH_API_KEY"
    echo ""
    echo "Run this script again after editing .env"
    exit 1
fi

echo "✅ .env file found"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if (( $(echo "$PYTHON_VERSION >= 3.10" | bc -l) )); then
    echo "✅ Python $PYTHON_VERSION detected"
else
    echo "❌ Python 3.10+ required (found $PYTHON_VERSION)"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if command -v poetry &> /dev/null; then
    echo "   Using Poetry"
    poetry install
else
    echo "   Using pip"
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Create corpora: python setup_corpus.py --create-all"
echo "   2. Upload documents: python ingestion/client_ingestion_adapter.py --client-id CLIENT_ID"
echo "   3. Grant permissions: bash deployment/grant_permissions.sh"
echo "   4. Deploy agents: python deployment/deploy_all_agents.py"
echo ""
echo "📖 Full guide: cat SETUP_GUIDE.md"
