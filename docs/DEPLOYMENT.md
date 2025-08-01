# Flask API Deployment Guide

## Free Hosting Options

### 1. Render (Recommended)
**Domain**: `remindly.onrender.com`

#### Steps:
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `task-manager-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables:
   - `JWT_SECRET_KEY`: Your secret key
   - `SECRET_KEY`: Your Flask secret key
6. Deploy!

### 2. Railway
**Domain**: `your-app-name.railway.app`

#### Steps:
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Add environment variables in the dashboard

### 3. PythonAnywhere
**Domain**: `your-username.pythonanywhere.com`

#### Steps:
1. Go to [pythonanywhere.com](https://pythonanywhere.com) and sign up
2. Go to "Web" tab → "Add a new web app"
3. Choose "Flask" and Python 3.11
4. Upload your files or clone from GitHub
5. Install requirements: `pip install -r requirements.txt`
6. Configure WSGI file to point to your app

## Environment Variables

Set these in your hosting platform:

```bash
JWT_SECRET_KEY=your_super_secret_jwt_key_here
SECRET_KEY=your_super_secret_flask_key_here
FLASK_ENV=production
```

## Database Considerations

Your current setup uses SQLite. For production, consider:

1. **Keep SQLite** (simple, works for small apps)
2. **Upgrade to PostgreSQL** (recommended for production)
3. **Use cloud database** (AWS RDS, Railway Postgres, etc.)

## Testing Your Deployment

After deployment, test these endpoints:

- `GET /` - API status
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/tasks` - Get tasks (requires auth)

## Custom Domain (Optional)

If you want a custom domain later:
1. Buy domain from Namecheap, GoDaddy, etc.
2. Configure DNS to point to your hosting platform
3. Add domain in hosting platform settings

## Monitoring

- Check your hosting platform's logs
- Monitor API response times
- Set up error notifications

## Security Notes

- Change default secret keys
- Enable HTTPS (automatic on most platforms)
- Consider rate limiting for production
- Regularly update dependencies 