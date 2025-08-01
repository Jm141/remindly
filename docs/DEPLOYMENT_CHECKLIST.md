# ✅ Deployment Checklist

## Pre-Deployment
- [x] ✅ All required files present (app.py, requirements.txt, Procfile, runtime.txt)
- [x] ✅ Code is working locally
- [x] ✅ Repository is pushed to GitHub

## Environment Variables (Set in hosting platform)
- [ ] JWT_SECRET_KEY=K8m#nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM#8nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM
- [ ] SECRET_KEY=H7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA#7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA
- [ ] FLASK_ENV=production

## Render Deployment Steps
- [ ] Go to [render.com](https://render.com)
- [ ] Sign up with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure service:
  - Name: `remindly-api`
  - Environment: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`
  - Plan: `Free`
- [ ] Add environment variables
- [ ] Click "Create Web Service"
- [ ] Wait for deployment

## Post-Deployment Testing
- [ ] Test health check: `https://your-app-name.onrender.com/`
- [ ] Test API status: `https://your-app-name.onrender.com/api/`
- [ ] Test user registration
- [ ] Test user login
- [ ] Test task creation (requires auth)

## Your Deployment URL
- [ ] **Render**: `https://remindly-api.onrender.com`
- [ ] **Railway**: `https://remindly-api.railway.app`
- [ ] **Vercel**: `https://remindly-api.vercel.app`

## Notes
- Environment variables are NOT set locally (this is normal)
- They will be set in the hosting platform dashboard
- Your API will be available at the URL above once deployed
- Free tier has some limitations but works great for development/testing 