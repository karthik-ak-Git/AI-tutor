# Deploy AI Tutor API to Render - Step by Step Guide

## Quick Deploy (5 minutes)

### Step 1: Prepare Your Code

1. **Make sure all files are committed to Git:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Verify these files exist:**
   - ✅ `render.yaml` (for automatic setup)
   - ✅ `requirements.txt`
   - ✅ `app/` directory with all code
   - ✅ `.env.example` (for reference)

### Step 2: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Sign up (free account works)
3. Connect your GitHub account

### Step 3: Deploy Using Blueprint (Easiest)

1. **In Render Dashboard:**
   - Click **"New +"** button (top right)
   - Select **"Blueprint"**

2. **Connect Repository:**
   - Select your GitHub account
   - Choose the repository: `AI-tutor`
   - Click **"Connect"**

3. **Review Configuration:**
   - Render will detect `render.yaml`
   - Review the settings (they're pre-configured)
   - Click **"Apply"**

4. **Set Environment Variable:**
   - After deployment starts, go to your service
   - Click **"Environment"** tab
   - Add environment variable:
     - **Key**: `OPENROUTER_API_KEY`
     - **Value**: Your actual API key (click "Encrypt" to mark as secret)
   - Click **"Save Changes"**

5. **Wait for Deployment:**
   - First build takes 5-10 minutes
   - Watch the logs for progress
   - Service will be live at: `https://your-app-name.onrender.com`

### Step 4: Manual Setup (Alternative)

If Blueprint doesn't work, use manual setup:

1. **Create Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository

2. **Configure Settings:**
   - **Name**: `ai-tutor-api` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables:**
   Click **"Advanced"** → **"Add Environment Variable"**:
   
   **Required:**
   ```
   OPENROUTER_API_KEY=sk-or-your-key-here
   ```
   
   **Optional (with defaults):**
   ```
   OPENROUTER_MODEL=openai/gpt-4.1-nano
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_TEMPERATURE=0.5
   OPENROUTER_TIMEOUT=30
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   EMBEDDING_DEVICE=cpu
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   RETRIEVER_K=4
   SEARCH_MAX_RESULTS=10
   DEBUG=false
   LOG_LEVEL=INFO
   ```

4. **Create Service:**
   - Click **"Create Web Service"**
   - Wait for deployment

## Post-Deployment

### 1. Test Your API

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test chat
curl -X POST https://your-app-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### 2. Access Frontend

Open in browser: `https://your-app-name.onrender.com`

### 3. Access API Docs

- Swagger UI: `https://your-app-name.onrender.com/docs`
- ReDoc: `https://your-app-name.onrender.com/redoc`

## Important Notes

### Free Tier Limitations

⚠️ **Render Free Tier:**
- **Spins down** after 15 minutes of inactivity
- **First request** after spin-down takes ~30 seconds
- **512MB RAM** limit
- **Ephemeral storage** (files lost on restart)

### Persistent Storage

**Problem:** Uploaded files and ChromaDB data will be lost on restart.

**Solutions:**

1. **Upgrade to Paid Plan** ($7/month):
   - Always-on service
   - Persistent disk available
   - Better performance

2. **Use External Storage:**
   - Upload files to S3/Cloudinary
   - Use Pinecone/Weaviate for vector DB
   - Store data in external database

3. **Accept Limitations:**
   - Documents must be re-uploaded after restart
   - Use for testing/demos only

### Build Time

First build takes 5-10 minutes because:
- Installing sentence-transformers (large package)
- Downloading embedding models
- Installing all dependencies

This is normal! Subsequent deployments are faster.

### Memory Issues

If you get memory errors:
- Upgrade to paid plan (more RAM)
- Use smaller embedding models
- Reduce chunk sizes in settings

## Troubleshooting

### Build Fails

**Check:**
1. All dependencies in `requirements.txt`
2. Python version compatibility
3. Build logs for specific errors

**Fix:**
```bash
# Test locally first
pip install -r requirements.txt
python run.py
```

### Service Crashes

**Check logs:**
1. Go to service → **"Logs"** tab
2. Look for error messages
3. Common issues:
   - Missing `OPENROUTER_API_KEY`
   - Memory limit exceeded
   - Import errors

### Slow Response Times

**Free tier spins down:**
- First request after 15 min: ~30 seconds
- Subsequent requests: normal speed
- **Solution:** Upgrade to paid plan for always-on

### Frontend Not Loading

**Check:**
1. `frontend/` directory exists in repo
2. Files are committed to Git
3. Check logs for file serving errors

## Environment Variables Reference

Copy these to Render dashboard:

```env
# Required
OPENROUTER_API_KEY=sk-or-your-actual-key

# Optional (defaults shown)
OPENROUTER_MODEL=openai/gpt-4.1-nano
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_TEMPERATURE=0.5
OPENROUTER_TIMEOUT=30
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DEVICE=cpu
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVER_K=4
SEARCH_MAX_RESULTS=10
DEBUG=false
LOG_LEVEL=INFO
```

## Updating Deployment

### Automatic Updates

Render automatically deploys when you push to your connected branch.

### Manual Deploy

1. Go to service dashboard
2. Click **"Manual Deploy"**
3. Select branch
4. Click **"Deploy"**

## Cost Estimate

- **Free Tier**: $0/month (with limitations)
- **Starter Plan**: $7/month (always-on, 512MB RAM)
- **Standard Plan**: $25/month (always-on, 2GB RAM)

## Security Checklist

- [ ] API keys marked as "Encrypt" in Render
- [ ] CORS configured for production (update in `app/main.py`)
- [ ] No sensitive data in code
- [ ] Environment variables set correctly

## Quick Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] `render.yaml` exists
- [ ] `requirements.txt` is complete
- [ ] `.env` file NOT committed (in `.gitignore`)
- [ ] OpenRouter API key ready

After deploying:
- [ ] Service shows "Live" status
- [ ] Health check works (`/health`)
- [ ] Frontend loads (`/`)
- [ ] API docs accessible (`/docs`)
- [ ] Can send test message

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Your API: `https://your-app-name.onrender.com/docs`

## Your Deployed URLs

After deployment, you'll have:
- **Frontend**: `https://your-app-name.onrender.com`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`

That's it! Your AI Tutor API is now live on Render! 🚀

