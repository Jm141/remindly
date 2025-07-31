# 🚀 Flask API Deployment Guide - Free Domains

## Quick Deploy Options

### Option 1: Render (Recommended) ⭐
**Free Domain**: `remindly-api.onrender.com`

### Option 2: Railway 
**Free Domain**: `remindly-api.railway.app`

### Option 3: Vercel
**Free Domain**: `remindly-api.vercel.app`

---

## 🎯 Render Deployment (Step-by-Step)

### Step 1: Prepare Your Repository
1. Make sure your code is pushed to GitHub
2. Ensure these files are in your root directory:
   - `app.py` ✅
   - `requirements.txt` ✅
   - `Procfile` ✅
   - `runtime.txt` ✅

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `remindly-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

### Step 3: Add Environment Variables
In Render dashboard, go to **Environment** tab and add:
```
JWT_SECRET_KEY=K8m#nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM#8nP$2vL@9qR!5wX&7yZ*4cF%6hJ^3kM
SECRET_KEY=H7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA#7j#kL$9mN@2pQ!6rS&8tU*5vW%1xY^4zA
FLASK_ENV=production
```

### Step 4: Deploy!
Click **"Create Web Service"** and wait for deployment.

**Your API will be available at**: `https://remindly-api.onrender.com`

---

## 🚂 Railway Deployment (Alternative)

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect Python and deploy

### Step 2: Add Environment Variables
In Railway dashboard, add the same environment variables as above.

**Your API will be available at**: `https://remindly-api.railway.app`

---

## 🧪 Test Your Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app-name.onrender.com/

# API status
curl https://your-app-name.onrender.com/api/

# Register a user
curl -X POST https://your-app-name.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **Build fails**: Check `requirements.txt` has all dependencies
2. **App crashes**: Check logs in hosting platform dashboard
3. **Environment variables**: Ensure they're set correctly
4. **Database issues**: SQLite works fine for small apps

### Check Logs:
- **Render**: Go to your service → **Logs** tab
- **Railway**: Go to your project → **Deployments** → **View Logs**

---

## 🌐 Custom Domain (Optional)

Want a custom domain later?

1. **Buy domain** from Namecheap, GoDaddy, etc.
2. **Configure DNS** to point to your hosting platform
3. **Add domain** in hosting platform settings

---

## 📊 Monitoring Your API

### Free Monitoring Tools:
- **UptimeRobot**: Monitor API availability
- **Postman**: Test API endpoints
- **Render/Railway Dashboard**: View logs and performance

### Health Check Endpoint:
Your API includes a health check at `/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "2.0.0"
}
```

---

## 🔒 Security Notes

✅ **Already configured**:
- JWT authentication
- CORS protection
- Environment variables
- HTTPS (automatic on hosting platforms)

⚠️ **For production**:
- Consider rate limiting
- Add API key authentication
- Monitor for suspicious activity
- Regular dependency updates

---

## 📱 API Endpoints

Your deployed API will have these endpoints:

- `GET /` - API status
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/tasks` - Get tasks (requires auth)
- `POST /api/tasks` - Create task (requires auth)
- `PUT /api/tasks/<id>` - Update task (requires auth)
- `DELETE /api/tasks/<id>` - Delete task (requires auth)
- `GET /health` - Health check

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Free hosting
- ✅ Free domain
- ✅ SSL certificate
- ✅ Auto-deployment from GitHub
- ✅ Professional API endpoint

**Example URLs**:
- `https://remindly-api.onrender.com`
- `https://remindly-api.railway.app`
- `https://remindly-api.vercel.app`

Choose the one you prefer and follow the steps above! 