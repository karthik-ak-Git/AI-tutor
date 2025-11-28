# Deployment Guide - AI Tutor API

Complete deployment guide for the AI Tutor FastAPI application.

## 🚀 Quick Deploy to Render

### Method 1: Using Blueprint (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically
   - Click **"Apply"**

3. **Set Environment Variable**:
   - Go to your service → **"Environment"** tab
   - Add: `OPENROUTER_API_KEY` = Your API key (mark as secret)
   - Click **"Save Changes"**

4. **Wait for Deployment**:
   - First build takes 5-10 minutes
   - Service will be live at: `https://your-app-name.onrender.com`

### Method 2: Manual Setup

1. **Create Web Service**:
   - Click **"New +"** → **"Web Service"**
   - Connect GitHub repository

2. **Configure**:
   - **Name**: `ai-tutor-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**:
   ```
   OPENROUTER_API_KEY=sk-or-your-key-here
   ```

## 📋 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `render.yaml` exists
- [ ] `requirements.txt` is complete
- [ ] `.env` file NOT committed
- [ ] OpenRouter API key ready
- [ ] Health check works (`/health`)

## 🔧 Environment Variables

**Required**:
- `OPENROUTER_API_KEY` - Your OpenRouter API key

**Optional** (with defaults):
- `OPENROUTER_MODEL=openai/gpt-4.1-nano`
- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`
- `OPENROUTER_TEMPERATURE=0.5`
- `EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`
- `LOG_LEVEL=INFO`

## ⚠️ Free Tier Limitations

- **Spins down** after 15 minutes of inactivity
- **First request** after spin-down takes ~30 seconds
- **Ephemeral storage** (files lost on restart)

**Solutions**:
- Upgrade to paid plan ($7/month) for persistent storage
- Use external storage (S3, Pinecone) for production

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t ai-tutor:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e OPENROUTER_API_KEY=your-key \
  ai-tutor:latest
```

## ✅ Post-Deployment

1. **Test Health**: `https://your-app.onrender.com/health`
2. **API Docs**: `https://your-app.onrender.com/docs`
3. **Frontend**: `https://your-app.onrender.com`

## 🔍 Troubleshooting

- **Build fails**: Check `requirements.txt` and logs
- **Service crashes**: Verify `OPENROUTER_API_KEY` is set
- **Slow response**: Normal on free tier (spins down)

## 📚 More Information

- Render Docs: https://render.com/docs
- API Documentation: `/docs` endpoint
- Health Check: `/health` endpoint
