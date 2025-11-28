# Deploying AI Tutor API to Render

This guide will help you deploy the AI Tutor FastAPI application to Render.

## Prerequisites

1. A [Render](https://render.com) account (free tier available)
2. Your OpenRouter API key
3. GitHub repository with your code (or use Render's direct deploy)

## Deployment Methods

### Method 1: Using render.yaml (Recommended)

This is the easiest method using Infrastructure as Code.

#### Step 1: Push to GitHub

```bash
# Make sure your code is in a GitHub repository
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

#### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Review the configuration and click **"Apply"**

#### Step 3: Set Environment Variables

1. Go to your service settings
2. Navigate to **"Environment"** tab
3. Add your `OPENROUTER_API_KEY`:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your actual API key (mark as secret)
4. Render will use other defaults from `render.yaml`

#### Step 4: Deploy

Render will automatically:
- Build your application
- Install dependencies
- Start the service
- Health check at `/health`

### Method 2: Manual Web Service Setup

If you prefer manual setup:

#### Step 1: Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository and branch

#### Step 2: Configure Build Settings

- **Name**: `ai-tutor-api` (or your preferred name)
- **Region**: Choose closest to you (Oregon, Frankfurt, etc.)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or specify if needed)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Set Environment Variables

Add these environment variables in the Render dashboard:

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

#### Step 4: Deploy

Click **"Create Web Service"** and Render will:
1. Clone your repository
2. Install dependencies
3. Start your application
4. Provide a public URL

## Important Notes for Render

### 1. Port Configuration

Render automatically sets the `PORT` environment variable. Your app should use:
```python
port = int(os.getenv("PORT", 8000))
```

The `render.yaml` and `app/main.py` already handle this correctly.

### 2. Persistent Storage

**Important**: Render's free tier has **ephemeral disk storage**. This means:
- Files uploaded to `uploads/` will be lost on restart
- ChromaDB data in `chroma_db/` will be lost on restart

**Solutions:**
- Use Render's **Disk** add-on (paid) for persistent storage
- Use external storage (S3, Cloudinary, etc.) for file uploads
- Use external vector database (Pinecone, Weaviate, etc.) instead of ChromaDB

### 3. Build Time

The first build may take 5-10 minutes because:
- Installing sentence-transformers (large package)
- Downloading embedding models
- Installing all dependencies

### 4. Memory Limits

Free tier has 512MB RAM. If you encounter memory issues:
- Upgrade to paid plan
- Use smaller embedding models
- Reduce chunk sizes

### 5. Health Check

The app includes a health check endpoint at `/health` which Render uses to verify the service is running.

## Post-Deployment

### 1. Test Your API

```bash
# Health check
curl https://your-app.onrender.com/health

# Test chat endpoint
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### 2. Access API Documentation

Visit: `https://your-app.onrender.com/docs`

### 3. Monitor Logs

- Go to your service in Render dashboard
- Click **"Logs"** tab
- Monitor for errors or issues

## Troubleshooting

### Build Fails

**Issue**: Build timeout or memory error
**Solution**: 
- Upgrade to paid plan
- Reduce dependencies
- Use lighter models

### Service Crashes

**Issue**: Service starts then crashes
**Solution**:
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `OPENROUTER_API_KEY` is correct

### Slow Response Times

**Issue**: API responses are slow
**Solution**:
- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Upgrade to paid plan for always-on service

### File Upload Issues

**Issue**: Uploaded files disappear
**Solution**:
- Use external storage (S3, Cloudinary)
- Implement file upload to external service
- Use Render Disk add-on for persistent storage

## Updating Your Deployment

### Automatic Deploys

Render automatically deploys when you push to your connected branch.

### Manual Deploy

1. Go to your service
2. Click **"Manual Deploy"**
3. Select branch and click **"Deploy"**

## Environment-Specific Configuration

For production, consider:

1. **CORS Settings**: Update `allow_origins` in `app/main.py` to your frontend domain
2. **Rate Limiting**: Add rate limiting middleware
3. **API Keys**: Use Render's secret management
4. **Monitoring**: Add APM tools
5. **Logging**: Configure centralized logging

## Cost Considerations

- **Free Tier**: 
  - 750 hours/month
  - Spins down after 15 min inactivity
  - 512MB RAM
  - Ephemeral storage

- **Starter Plan ($7/month)**:
  - Always on
  - 512MB RAM
  - Persistent disk available

- **Standard Plan ($25/month)**:
  - Always on
  - 2GB RAM
  - Better performance

## Alternative: Using Docker

If you prefer Docker deployment:

1. Render supports Docker
2. Use the provided `Dockerfile`
3. Set build command: `docker build -t ai-tutor .`
4. Set start command: `docker run -p $PORT:8000 ai-tutor`

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Your API Docs: `https://your-app.onrender.com/docs`

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected
- [ ] Environment variables set (especially `OPENROUTER_API_KEY`)
- [ ] Service deployed
- [ ] Health check passing (`/health`)
- [ ] API docs accessible (`/docs`)
- [ ] Test endpoint working

Your API will be live at: `https://your-app-name.onrender.com`


