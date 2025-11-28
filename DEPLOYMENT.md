# Deployment Guide - AI Tutor API

Quick deployment guide for various platforms.

## 🚀 Render Deployment (Recommended)

See [RENDER_DEPLOY.md](./RENDER_DEPLOY.md) for detailed instructions.

### Quick Start:
1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Blueprint"
4. Connect repository
5. Set `OPENROUTER_API_KEY` environment variable
6. Deploy!

## 📋 Pre-Deployment Checklist

- [ ] All code committed and pushed to GitHub
- [ ] Environment variables documented
- [ ] `.env` file NOT committed (in `.gitignore`)
- [ ] API keys secured
- [ ] Dependencies in `requirements.txt`
- [ ] Health check endpoint working (`/health`)
- [ ] CORS configured for production

## 🔧 Environment Variables

Required:
- `OPENROUTER_API_KEY` - Your OpenRouter API key

Optional (with defaults):
- `OPENROUTER_MODEL` - Model name (default: `openai/gpt-4.1-nano`)
- `PORT` - Server port (auto-set by platform)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## 📝 Platform-Specific Notes

### Render
- Free tier: Spins down after 15 min inactivity
- Use `render.yaml` for Infrastructure as Code
- Persistent storage requires paid plan

### Heroku
- Use `Procfile` for process definition
- Add `runtime.txt` for Python version
- Use Heroku Postgres for database (if needed)

### Railway
- Similar to Render
- Automatic deployments from GitHub
- Persistent volumes available

### Fly.io
- Docker-based deployment
- Global edge deployment
- Persistent volumes available

## 🔒 Security Checklist

- [ ] API keys in environment variables (not code)
- [ ] CORS configured for specific domains
- [ ] Rate limiting implemented (recommended)
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS enabled (automatic on most platforms)

## 📊 Monitoring

After deployment:
1. Test health endpoint: `GET /health`
2. Check API docs: `GET /docs`
3. Monitor logs for errors
4. Test main endpoints
5. Set up uptime monitoring (optional)

## 🐛 Troubleshooting

### Service won't start
- Check logs for errors
- Verify environment variables
- Check port configuration
- Ensure dependencies installed

### Build fails
- Check Python version compatibility
- Verify `requirements.txt` is correct
- Check build logs for specific errors
- Ensure all dependencies are listed

### Memory issues
- Upgrade to higher tier
- Reduce chunk sizes
- Use lighter models
- Optimize code

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Documentation](https://www.uvicorn.org/)


