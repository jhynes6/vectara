"""
Flask Web UI for Inbox Manager
"""
from flask import Flask, render_template, request, jsonify, session
import logging
import json
from datetime import datetime

from email_handler import EmailHandler
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change in production!

# Initialize handlers
vector_store = VectorStore()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Get list of available clients"""
    try:
        clients = vector_store.list_available_clients()
        
        # Get document counts for each client
        client_data = []
        for client_id in clients:
            doc_count = vector_store.get_client_documents_count(client_id)
            client_data.append({
                'id': client_id,
                'name': client_id.replace('-', ' ').replace('_', ' ').title(),
                'document_count': doc_count
            })
        
        return jsonify({
            'success': True,
            'clients': client_data
        })
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/handle-email', methods=['POST'])
def handle_email():
    """Handle customer email and generate response"""
    try:
        data = request.json
        
        email_content = data.get('email_content', '').strip()
        client_id = data.get('client_id', '').strip()
        client_name = data.get('client_name', '').strip()
        llm_provider = data.get('llm_provider', 'openai')
        enable_verification = data.get('enable_verification', True)
        
        # Validation
        if not email_content:
            return jsonify({
                'success': False,
                'error': 'Email content is required'
            }), 400
        
        if not client_id:
            return jsonify({
                'success': False,
                'error': 'Client ID is required'
            }), 400
        
        # Initialize handler with selected LLM
        handler = EmailHandler(llm_provider=llm_provider)
        
        # Process email
        logger.info(f"Processing email for client_id={client_id}, llm={llm_provider}")
        result = handler.handle_email(
            email_content=email_content,
            client_id=client_id,
            client_name=client_name or client_id,
            enable_verification=enable_verification
        )
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error handling email: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-documents', methods=['POST'])
def search_documents():
    """Search documents in knowledge base"""
    try:
        data = request.json
        
        query = data.get('query', '').strip()
        client_id = data.get('client_id', '').strip()
        top_k = data.get('top_k', 5)
        
        if not query or not client_id:
            return jsonify({
                'success': False,
                'error': 'Query and client_id are required'
            }), 400
        
        # Search documents
        documents = vector_store.search_documents(
            query=query,
            client_id=client_id,
            top_k=top_k
        )
        
        # Format results
        results = []
        for doc in documents:
            results.append({
                'id': doc.get('id'),
                'content': doc.get('content', '')[:500] + '...',  # Truncate for display
                'similarity': doc.get('similarity'),
                'metadata': doc.get('metadata')
            })
        
        return jsonify({
            'success': True,
            'documents': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
