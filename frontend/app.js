// Configuration
const CONFIG = {
    apiEndpoint: localStorage.getItem('apiEndpoint') || 'http://localhost:8000',
    sessionId: localStorage.getItem('sessionId') || generateSessionId(),
    autoScroll: true
};

// Generate unique session ID
function generateSessionId() {
    return 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

// Save session ID to localStorage
localStorage.setItem('sessionId', CONFIG.sessionId);

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const attachBtn = document.getElementById('attachBtn');
const voiceBtn = document.getElementById('voiceBtn');
const useDocumentCheckbox = document.getElementById('useDocument');
const uploadModal = document.getElementById('uploadModal');
const settingsModal = document.getElementById('settingsModal');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const uploadArea = document.getElementById('uploadArea');
const loadingIndicator = document.getElementById('loadingIndicator');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkHealth();
});

// Initialize app
function initializeApp() {
    // Set session ID in settings
    document.getElementById('sessionId').value = CONFIG.sessionId;
    document.getElementById('apiEndpoint').value = CONFIG.apiEndpoint;
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Enable/disable send button
    messageInput.addEventListener('input', toggleSendButton);
    toggleSendButton();
}

// Setup event listeners
function setupEventListeners() {
    // Chat form submission
    chatForm.addEventListener('submit', handleSubmit);
    
    // Clear chat
    clearBtn.addEventListener('click', clearChat);
    
    // Attach document
    attachBtn.addEventListener('click', () => {
        uploadModal.classList.add('active');
    });
    
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Upload form
    uploadForm.addEventListener('submit', handleUpload);
    
    // Modal close buttons
    document.getElementById('closeModal').addEventListener('click', () => {
        uploadModal.classList.remove('active');
    });
    
    document.getElementById('closeSettings').addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });
    
    // Settings button
    document.getElementById('settingsBtn').addEventListener('click', () => {
        settingsModal.classList.add('active');
    });
    
    // New session
    document.getElementById('newSession').addEventListener('click', () => {
        CONFIG.sessionId = generateSessionId();
        localStorage.setItem('sessionId', CONFIG.sessionId);
        document.getElementById('sessionId').value = CONFIG.sessionId;
        clearChat();
    });
    
    // Save settings
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    
    // Cancel upload
    document.getElementById('cancelUpload').addEventListener('click', () => {
        uploadModal.classList.remove('active');
        fileInput.value = '';
    });
    
    // Close modals on outside click
    uploadModal.addEventListener('click', (e) => {
        if (e.target === uploadModal) {
            uploadModal.classList.remove('active');
        }
    });
    
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('active');
        }
    });
    
    // Voice button (placeholder)
    voiceBtn.addEventListener('click', () => {
        alert('Voice input coming soon!');
    });
}

// Auto-resize textarea
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 150) + 'px';
}

// Toggle send button
function toggleSendButton() {
    const hasValue = messageInput.value.trim().length > 0;
    sendBtn.disabled = !hasValue;
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input
    messageInput.value = '';
    autoResizeTextarea();
    toggleSendButton();
    
    // Show loading
    showLoading();
    
    try {
        // Determine endpoint based on useDocument checkbox
        const useDocument = useDocumentCheckbox.checked;
        const endpoint = useDocument ? '/learn/ask' : '/chat';
        
        const response = await fetch(`${CONFIG.apiEndpoint}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: CONFIG.sessionId,
                use_document: useDocument
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add assistant response
        addMessage('assistant', data.response, data.source);
        
        // Update session ID if provided
        if (data.session_id) {
            CONFIG.sessionId = data.session_id;
            localStorage.setItem('sessionId', CONFIG.sessionId);
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('assistant', `Error: ${error.message}. Please check your API endpoint and try again.`, 'error');
    } finally {
        hideLoading();
    }
}

// Add message to chat
function addMessage(role, content, source = null) {
    // Remove welcome message if exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'user' ? '👤' : '🤖';
    const author = role === 'user' ? 'You' : 'AI Tutor';
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    let sourceBadge = '';
    if (source && role === 'assistant') {
        const sourceLabels = {
            'document': '📚 Document',
            'web': '🌐 Web',
            'general': '💡 General',
            'error': '❌ Error'
        };
        sourceBadge = `<span class="message-source">${sourceLabels[source] || source}</span>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">${author}</span>
                ${sourceBadge}
                <span class="message-time">${time}</span>
            </div>
            <div class="message-text">${escapeHtml(content)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    if (CONFIG.autoScroll) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Clear chat
function clearChat() {
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">👋</div>
            <h2>Welcome to AI Tutor!</h2>
            <p>I can help you with:</p>
            <ul>
                <li>📚 Questions about uploaded documents</li>
                <li>🌐 General knowledge and current events</li>
                <li>💡 Learning and explanations</li>
            </ul>
            <p class="hint">Start by asking a question or uploading a document!</p>
        </div>
    `;
    
    // Clear session on backend
    fetch(`${CONFIG.apiEndpoint}/chat/${CONFIG.sessionId}`, {
        method: 'DELETE'
    }).catch(err => console.error('Error clearing session:', err));
}

// Handle file select
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        // Show file name in upload area
        uploadArea.innerHTML = `
            <div class="upload-placeholder">
                <p><strong>${file.name}</strong></p>
                <p class="upload-hint">Click to change file</p>
            </div>
        `;
    }
}

// Handle file upload
async function handleUpload(e) {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${CONFIG.apiEndpoint}/document/summary`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Show success message
        addMessage('assistant', 
            `✅ Document uploaded successfully!\n\n` +
            `📄 Pages loaded: ${data.pages_loaded}\n` +
            `📦 Chunks created: ${data.chunks_created}\n\n` +
            `You can now ask questions about this document!`,
            'document'
        );
        
        // Close modal and reset
        uploadModal.classList.remove('active');
        fileInput.value = '';
        uploadArea.innerHTML = `
            <div class="upload-placeholder">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <p>Click to upload or drag and drop</p>
                <p class="upload-hint">PDF or Text files only</p>
            </div>
        `;
        
    } catch (error) {
        console.error('Upload error:', error);
        alert(`Upload failed: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// Save settings
function saveSettings() {
    const endpoint = document.getElementById('apiEndpoint').value.trim();
    if (endpoint) {
        CONFIG.apiEndpoint = endpoint;
        localStorage.setItem('apiEndpoint', endpoint);
        settingsModal.classList.remove('active');
        checkHealth();
    }
}

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(`${CONFIG.apiEndpoint}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('API Health:', data);
        }
    } catch (error) {
        console.warn('API health check failed:', error);
        addMessage('assistant', 
            `⚠️ Warning: Could not connect to API at ${CONFIG.apiEndpoint}. ` +
            `Please check your settings and ensure the backend is running.`,
            'error'
        );
    }
}

// Show loading indicator
function showLoading() {
    loadingIndicator.style.display = 'flex';
}

// Hide loading indicator
function hideLoading() {
    loadingIndicator.style.display = 'none';
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to send
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (messageInput === document.activeElement) {
            chatForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        uploadModal.classList.remove('active');
        settingsModal.classList.remove('active');
    }
});

