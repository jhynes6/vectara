#!/bin/bash
# Grant RAG Corpus query permissions to Vertex AI Agent Engine Service Agent
# Based on the RAG sample implementation

set -e

# Load environment variables
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
else
    echo "❌ Error: .env file not found"
    echo "💡 Please run setup_corpus.py first to create corpora"
    exit 1
fi

# Check required variables
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ Error: GOOGLE_CLOUD_PROJECT not set in .env"
    exit 1
fi

if [ -z "$RAG_CORPUS_MAIN" ]; then
    echo "❌ Error: RAG_CORPUS_MAIN not set in .env"
    echo "💡 Run setup_corpus.py to create corpora first"
    exit 1
fi

echo "🔐 Granting RAG Corpus permissions..."
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "="
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Corpus: $RAG_CORPUS_MAIN"

# Get project number
PROJECT_NUMBER=$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format="value(projectNumber)")
echo "Project Number: $PROJECT_NUMBER"

# Service account for Vertex AI Reasoning Engine
SERVICE_ACCOUNT="service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
echo "Service Account: $SERVICE_ACCOUNT"

# Create custom IAM role for RAG corpus query if it doesn't exist
echo ""
echo "📝 Creating custom IAM role (if not exists)..."
ROLE_NAME="ragCorpusQueryRole"
ROLE_TITLE="RAG Corpus Query Role"
ROLE_DESCRIPTION="Allows querying RAG corpora for AI agents"

if ! gcloud iam roles describe "$ROLE_NAME" --project="$GOOGLE_CLOUD_PROJECT" &>/dev/null; then
    gcloud iam roles create "$ROLE_NAME" \
        --project="$GOOGLE_CLOUD_PROJECT" \
        --title="$ROLE_TITLE" \
        --description="$ROLE_DESCRIPTION" \
        --permissions=aiplatform.ragCorpora.query,aiplatform.ragFiles.get,aiplatform.ragFiles.list \
        --stage=GA
    echo "✅ Created custom role: $ROLE_NAME"
else
    echo "✅ Custom role already exists: $ROLE_NAME"
fi

# Grant the role to the service account
echo ""
echo "🔗 Binding role to service account..."
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="projects/$GOOGLE_CLOUD_PROJECT/roles/$ROLE_NAME" \
    --condition=None

echo ""
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "="
echo "✅ Permissions granted successfully!"
echo ""
echo "💡 Your agents can now query the RAG corpus"
echo "💡 Next steps:"
echo "   1. Deploy agents: python deployment/deploy_all_agents.py"
echo "   2. Test agents: python deployment/test_all_agents.py"
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "="

