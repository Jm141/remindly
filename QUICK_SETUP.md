# ⚡ Quick Render Setup Guide

## 🎯 Follow These Exact Steps

### 1. Go to Render Dashboard
- Visit: https://render.com
- Sign in with GitHub
- Click **"New +"** → **"Web Service"**

### 2. Connect Repository
- Search for: `remindly` or `Jm141/remindly`
- Click on your repository
- Click **"Connect"**

### 3. Configure Settings

#### Basic Configuration:
```
Name: remindly-api
Environment: Python 3
Region: (choose closest)
Branch: main
Root Directory: (leave empty)
```

#### Build & Deploy:
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
Plan: Free
```

### 4. Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these 3 variables:

```
JWT_SECRET_KEY = K8m#nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM#8nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM
SECRET_KEY = H7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA#7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA
FLASK_ENV = production
```

### 5. Deploy!
- Click **"Create Web Service"**
- Wait 2-5 minutes
- Watch the logs

## ✅ Success Indicators

Your deployment is successful when you see:

```
==> Build successful 🎉
==> Deploying...
==> Running 'gunicorn --bind 0.0.0.0:$PORT app:app'
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
```

**Status should show: "Live" (green)**

## 🌐 Your API URL

Once deployed, your API will be at:
`https://remindly-api.onrender.com`

## 🧪 Test Your API

```bash
# Test the API
curl https://remindly-api.onrender.com/

# Test health check
curl https://remindly-api.onrender.com/health

# Test registration
curl -X POST https://remindly-api.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

## 🔧 If Something Goes Wrong

1. **Check the logs** in Render dashboard
2. **Verify environment variables** are set correctly
3. **Make sure your code is pushed** to GitHub
4. **Try manual deploy** if needed

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Check Status**: https://status.render.com
- **Community**: https://render.com/community

---

**That's it! Your Flask API will be live in minutes! 🚀** 