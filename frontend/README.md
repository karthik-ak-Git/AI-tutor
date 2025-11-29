# AI Tutor Frontend

Lightweight HTML/CSS/JavaScript chat interface for the AI Tutor API.

## Features

- 🎨 Modern, clean UI
- 💬 Real-time chat interface
- 📄 Document upload support
- 🔄 Session management
- ⚙️ Settings configuration
- 📱 Responsive design
- 🌙 Dark mode ready (CSS variables)

## Setup

### Option 1: Serve with FastAPI (Recommended)

The FastAPI backend automatically serves the frontend when placed in the `frontend/` directory.

1. Place frontend files in `frontend/` directory (already done)
2. Start the FastAPI server:
   ```bash
   python run.py
   ```
3. Open browser: `http://localhost:8000`

### Option 2: Serve Separately

If you want to serve the frontend separately:

1. Use any static file server:
   ```bash
   # Python
   cd frontend
   python -m http.server 3000
   
   # Node.js
   npx serve frontend
   
   # Or use any web server
   ```
2. Update API endpoint in settings (default: `http://localhost:8000`)

## Configuration

### API Endpoint

Default: `http://localhost:8000`

To change:
1. Click Settings (⚙️) button
2. Update "API Endpoint"
3. Click "Save Settings"

### Session Management

- Each session maintains conversation history
- Session ID is auto-generated and saved in localStorage
- Click "New Session" to start fresh

## Usage

### Chat

1. Type your message in the input box
2. Click send or press Ctrl/Cmd + Enter
3. Check "Use Document" to prefer document search

### Upload Document

1. Click attach button (📎)
2. Select PDF or text file
3. Wait for upload confirmation
4. Ask questions about the document

### Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Send message
- `Escape`: Close modals

## File Structure

```
frontend/
├── index.html      # Main HTML file
├── styles.css      # All styles
├── app.js          # Application logic
└── README.md       # This file
```

## Customization

### Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --background: #ffffff;
    /* ... */
}
```

### API Endpoints

The frontend uses these endpoints:
- `POST /chat` - General chat
- `POST /learn/ask` - Document-focused chat
- `POST /document/summary` - Upload document
- `DELETE /chat/{session_id}` - Clear session
- `GET /health` - Health check

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Troubleshooting

### Can't connect to API

1. Check API endpoint in settings
2. Ensure backend is running
3. Check CORS settings if serving separately
4. Check browser console for errors

### Upload not working

1. Check file size (max 50MB)
2. Ensure file is PDF or text
3. Check backend logs for errors

### Messages not appearing

1. Check browser console
2. Verify API endpoint
3. Check network tab for failed requests

## Production Deployment

### With FastAPI

The frontend is automatically served when deployed with FastAPI.

### Static Hosting

You can deploy the frontend to:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting

Just update the API endpoint to point to your deployed backend.

## Development

To modify the frontend:

1. Edit `index.html` for structure
2. Edit `styles.css` for styling
3. Edit `app.js` for functionality
4. Refresh browser to see changes

No build step required!


