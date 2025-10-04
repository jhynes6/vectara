// Inbox Manager Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Load clients on page load
    loadClients();

    // Event listeners
    document.getElementById('process-btn').addEventListener('click', processEmail);
    document.getElementById('clear-btn').addEventListener('click', clearForm);
    document.getElementById('search-btn').addEventListener('click', searchDocuments);
    document.getElementById('copy-btn')?.addEventListener('click', copyResponse);
    document.getElementById('new-email-btn')?.addEventListener('click', resetForm);

    // Enter key handling for search
    document.getElementById('search-query').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchDocuments();
        }
    });
});

async function loadClients() {
    const clientSelect = document.getElementById('client-select');
    const clientInfo = document.getElementById('client-info');
    
    try {
        const response = await fetch('/api/clients');
        const data = await response.json();
        
        if (data.success && data.clients.length > 0) {
            clientSelect.innerHTML = '<option value="">Select a client...</option>';
            
            data.clients.forEach(client => {
                const option = document.createElement('option');
                option.value = client.id;
                option.textContent = `${client.name} (${client.document_count} docs)`;
                option.dataset.name = client.name;
                option.dataset.count = client.document_count;
                clientSelect.appendChild(option);
            });

            // Update info on selection
            clientSelect.addEventListener('change', function() {
                const selected = this.options[this.selectedIndex];
                if (selected.value) {
                    clientInfo.textContent = `📚 ${selected.dataset.count} documents available`;
                } else {
                    clientInfo.textContent = '';
                }
            });
        } else {
            clientSelect.innerHTML = '<option value="">No clients found</option>';
            clientInfo.textContent = '⚠️ No clients with documents in database';
        }
    } catch (error) {
        console.error('Error loading clients:', error);
        clientSelect.innerHTML = '<option value="">Error loading clients</option>';
        showNotification('Failed to load clients', 'error');
    }
}

async function processEmail() {
    const emailContent = document.getElementById('email-content').value.trim();
    const clientSelect = document.getElementById('client-select');
    const clientId = clientSelect.value;
    const clientName = clientSelect.options[clientSelect.selectedIndex]?.dataset.name || clientId;
    const llmProvider = document.getElementById('llm-select').value;
    const enableVerification = document.getElementById('verification-check').checked;
    
    // Validation
    if (!emailContent) {
        showNotification('Please enter email content', 'error');
        return;
    }
    
    if (!clientId) {
        showNotification('Please select a client', 'error');
        return;
    }

    // Show loading state
    const processBtn = document.getElementById('process-btn');
    const btnText = processBtn.querySelector('.btn-text');
    const btnLoader = processBtn.querySelector('.btn-loader');
    
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    processBtn.disabled = true;

    try {
        const response = await fetch('/api/handle-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email_content: emailContent,
                client_id: clientId,
                client_name: clientName,
                llm_provider: llmProvider,
                enable_verification: enableVerification
            })
        });

        const data = await response.json();
        
        if (data.success) {
            displayResponse(data);
            showNotification('Response generated successfully!', 'success');
        } else {
            displayResponse(data);
            showNotification(data.error || 'Failed to generate response', 'warning');
        }
        
    } catch (error) {
        console.error('Error processing email:', error);
        showNotification('Network error: ' + error.message, 'error');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        processBtn.disabled = false;
    }
}

function displayResponse(data) {
    const responsePanel = document.getElementById('response-panel');
    const statusBadge = document.getElementById('status-badge');
    const responseContent = document.getElementById('response-content');
    
    // Show panel
    responsePanel.style.display = 'block';
    responsePanel.classList.add('fade-in');
    responsePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Status badge
    if (data.success) {
        statusBadge.className = 'status-badge success';
        statusBadge.textContent = '✅ Response Generated Successfully';
    } else {
        statusBadge.className = 'status-badge error';
        statusBadge.textContent = '⚠️ ' + (data.metadata?.reason || 'Could not generate response');
    }
    
    // Response content
    responseContent.textContent = data.response;
    
    // Metadata
    document.getElementById('meta-docs-found').textContent = data.documents_found || 0;
    
    const confidence = data.confidence || 0;
    const confidenceElement = document.getElementById('meta-confidence');
    confidenceElement.textContent = (confidence * 100).toFixed(1) + '%';
    confidenceElement.className = confidence > 0.8 ? 'confidence-high' : 
                                   confidence > 0.6 ? 'confidence-medium' : 
                                   'confidence-low';
    
    document.getElementById('meta-relevance').textContent = 
        data.metadata?.relevance_check || 'N/A';
    
    document.getElementById('meta-verification').textContent = 
        data.metadata?.verification || 'N/A';
    
    // Documents list
    if (data.metadata?.documents && data.metadata.documents.length > 0) {
        const docsList = document.getElementById('documents-list');
        docsList.innerHTML = '<h4 style="margin-bottom: 1rem;">📄 Source Documents</h4>';
        
        data.metadata.documents.forEach((doc, idx) => {
            const docItem = document.createElement('div');
            docItem.className = 'document-item';
            docItem.innerHTML = `
                <div class="document-header">
                    <span class="document-id">Document ${idx + 1}</span>
                    <span class="similarity-score">${(doc.similarity * 100).toFixed(1)}% match</span>
                </div>
                <div style="font-size: 0.875rem; color: var(--text-light);">
                    ${JSON.stringify(doc.metadata, null, 2)}
                </div>
            `;
            docsList.appendChild(docItem);
        });
    }
}

async function searchDocuments() {
    const query = document.getElementById('search-query').value.trim();
    const clientId = document.getElementById('client-select').value;
    const searchResults = document.getElementById('search-results');
    
    if (!query) {
        showNotification('Please enter a search query', 'error');
        return;
    }
    
    if (!clientId) {
        showNotification('Please select a client first', 'error');
        return;
    }

    // Show loading
    const searchBtn = document.getElementById('search-btn');
    const btnText = searchBtn.querySelector('.btn-text');
    const btnLoader = searchBtn.querySelector('.btn-loader');
    
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    searchBtn.disabled = true;

    try {
        const response = await fetch('/api/search-documents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                client_id: clientId,
                top_k: 5
            })
        });

        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.documents);
            showNotification(`Found ${data.count} documents`, 'success');
        } else {
            searchResults.innerHTML = '<p style="color: var(--error-color);">Search failed: ' + data.error + '</p>';
        }
        
    } catch (error) {
        console.error('Error searching:', error);
        searchResults.innerHTML = '<p style="color: var(--error-color);">Network error</p>';
    } finally {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        searchBtn.disabled = false;
    }
}

function displaySearchResults(documents) {
    const searchResults = document.getElementById('search-results');
    
    if (!documents || documents.length === 0) {
        searchResults.innerHTML = '<p style="color: var(--text-light);">No documents found</p>';
        return;
    }
    
    searchResults.innerHTML = '';
    
    documents.forEach((doc, idx) => {
        const resultItem = document.createElement('div');
        resultItem.className = 'search-result-item';
        resultItem.innerHTML = `
            <div class="search-result-header">
                <span class="document-id">Result ${idx + 1}</span>
                <span class="similarity-score">${(doc.similarity * 100).toFixed(1)}% match</span>
            </div>
            <div class="search-result-content">${doc.content}</div>
        `;
        searchResults.appendChild(resultItem);
    });
}

function clearForm() {
    document.getElementById('email-content').value = '';
    document.getElementById('response-panel').style.display = 'none';
}

function resetForm() {
    clearForm();
    document.getElementById('search-query').value = '';
    document.getElementById('search-results').innerHTML = '';
}

function copyResponse() {
    const responseText = document.getElementById('response-content').textContent;
    navigator.clipboard.writeText(responseText).then(() => {
        showNotification('Response copied to clipboard!', 'success');
    }).catch(err => {
        showNotification('Failed to copy', 'error');
    });
}

function showNotification(message, type = 'info') {
    // Simple notification - could be enhanced with a toast library
    const color = type === 'success' ? 'var(--success-color)' :
                  type === 'error' ? 'var(--error-color)' :
                  type === 'warning' ? 'var(--warning-color)' :
                  'var(--primary-color)';
    
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // You could add a toast notification here
    alert(message);
}
