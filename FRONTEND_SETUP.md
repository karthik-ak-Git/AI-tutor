# Frontend Setup Guide

## Quick Start

The frontend is already set up and ready to use! Just start the backend:

```bash
python run.py
```

Then open: `http://localhost:8000`

## Manual Setup (if needed)

### 1. Check Frontend Files

Ensure these files exist:
- `frontend/index.html`
- `frontend/styles.css`
- `frontend/app.js`

### 2. Verify FastAPI Configuration

The backend automatically serves the frontend. Check `app/main.py` - it should include:

```python
# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
```

### 3. Start Backend

```bash
python run.py
# or
uvicorn app.main:app --reload
```

### 4. Access Frontend

Open browser: `http://localhost:8000`

## Separate Frontend Server (Optional)

If you want to run frontend separately:

### Using Python

```bash
cd frontend
python -m http.server 3000
```

Then:
1. Open `http://localhost:3000`
2. Go to Settings
3. Update API endpoint to `http://localhost:8000`

### Using Node.js

```bash
npx serve frontend
```

### Using Live Server (VS Code)

1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

## Configuration

### Change API Endpoint

1. Click ⚙️ Settings button
2. Update "API Endpoint" field
3. Click "Save Settings"

### Default Settings

- API Endpoint: `http://localhost:8000`
- Session ID: Auto-generated
- Auto-scroll: Enabled

## Features

✅ Chat interface
✅ Document upload
✅ Session management
✅ Settings panel
✅ Responsive design
✅ Keyboard shortcuts

## Troubleshooting

### Frontend not loading

1. Check `frontend/` directory exists
2. Verify files are present
3. Check backend logs
4. Try accessing directly: `http://localhost:8000/static/index.html`

### API connection errors

1. Verify backend is running
2. Check API endpoint in settings
3. Check CORS settings if serving separately
4. Check browser console for errors

### Styling issues

1. Clear browser cache
2. Check CSS file is loading
3. Verify no JavaScript errors in console

## Production

For production deployment:

1. The frontend is automatically served with FastAPI
2. No additional configuration needed
3. Just deploy the backend and frontend together

## Customization

See `frontend/README.md` for customization options.

