# Deployment Guide - Discord Clone

This guide covers deploying the Discord Clone application to production.

## Prerequisites

- GitHub account and repository
- Render or Railway account for backend
- Vercel or Netlify account for frontend
- PostgreSQL database (managed)
- Redis instance (optional, for advanced features)

## Backend Deployment (Render)

### Step 1: Prepare Your Repository

Ensure your code is pushed to GitHub with a `.env` file (not committed):

```bash
# Add to .gitignore if not already there
echo ".env" >> .gitignore
echo "uploads/" >> .gitignore
echo "bot_data/" >> .gitignore
git add .
git commit -m "Prepare for deployment"
git push
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your GitHub account

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Configure:
   - Name: `discord-clone-db`
   - Region: Choose closest to you
   - PostgreSQL Version: 14
4. Click "Create Database"
5. Copy the connection string

### Step 4: Deploy Backend

1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Choose your Discord-clone repository
4. Configure:
   - Name: `discord-clone-api`
   - Environment: Python 3.11
   - Region: Same as database
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Root Directory: `backend`

5. Add Environment Variables:
   ```
   DATABASE_URL=postgresql://username:password@host/discord_clone
   SECRET_KEY=<generate-a-random-secret-key>
   ALGORITHM=HS256
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

6. Click "Create Web Service"

### Step 5: Verify Backend Deployment

Once deployed:

```bash
curl https://your-discord-clone-api.onrender.com/
# Should return: {"message": "Welcome to the Discord Clone API"}

# Check API docs
# https://your-discord-clone-api.onrender.com/docs
```

## Backend Deployment (Railway)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Create PostgreSQL Database

1. In Railway dashboard, click "New"
2. Select "Database"
3. Choose PostgreSQL
4. The database will be created automatically

### Step 3: Deploy Backend

1. Click "New"
2. Select "GitHub Repo"
3. Choose your Discord-clone repository
4. Configure:
   - Root Directory: `backend`

5. In the environment variables, add:
   ```
   DATABASE_URL=<auto-populated from PostgreSQL>
   SECRET_KEY=<generate-a-random-secret-key>
   ALGORITHM=HS256
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

6. Add a start command in your project's `Procfile` (create in backend/):
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

7. Deploy

## Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Deploy Frontend

1. In Vercel dashboard, click "Add New..."
2. Select "Project"
3. Import your GitHub repository
4. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

5. Add Environment Variables:
   ```
   VITE_API_URL=https://your-discord-clone-api.onrender.com
   ```

6. Click "Deploy"

## Frontend Deployment (Netlify)

### Step 1: Connect to Netlify

1. Go to https://netlify.com
2. Sign up with GitHub
3. Click "Add new site"
4. Select "Import an existing project"
5. Choose your GitHub repository

### Step 2: Configure Build Settings

1. Build Command: `npm run build`
2. Publish directory: `frontend/dist`
3. Environment Variables:
   ```
   VITE_API_URL=https://your-discord-clone-api.onrender.com
   ```

4. Deploy

### Step 3: Configure Redirects (Netlify)

Create `frontend/public/_redirects` file:

```
/*  /index.html  200
```

This ensures React Router works correctly.

## Post-Deployment Checklist

- [ ] Backend API is accessible
- [ ] Frontend loads without errors
- [ ] Can register a new account
- [ ] Can login successfully
- [ ] Can create servers and channels
- [ ] Can send and receive messages in real-time
- [ ] Can upload files
- [ ] File uploads are accessible
- [ ] Bot responds to questions
- [ ] Environment variables are set correctly
- [ ] CORS is properly configured

## Monitoring & Maintenance

### View Logs

**Render:**
```bash
# In Render dashboard, click on service > Logs
```

**Railway:**
```bash
# In Railway dashboard, click on service > Logs
```

### Database Backups

- Render: Automatic backups enabled by default
- Railway: Configure backups in database settings

### Performance

Monitor:
- API response times
- WebSocket connections
- File upload sizes
- Message delivery rates

### Updates

To update production:

1. Test changes locally
2. Push to GitHub
3. Render/Railway will auto-deploy (if connected)

## Troubleshooting

### WebSocket Connection Fails

- Check CORS origin in backend .env
- Verify frontend is using correct API URL
- Check firewall/proxy settings

### File Uploads Don't Work

- Verify `/uploads` directory exists on server
- Check file size limits
- Verify write permissions

### Database Connection Error

- Verify DATABASE_URL is correct
- Check database is accessible
- Verify credentials are correct

### Bot Not Working

- Check FAISS is installed
- Verify bot_data directory has bot files
- Check server logs for errors

## Scaling Considerations

### For Production Scale-up

1. **Add Redis for Caching**
   - Cache user servers/channels
   - Cache message history

2. **Add CDN for Files**
   - Use AWS S3 or Cloudflare R2
   - Store file uploads in CDN

3. **Database Optimization**
   - Add indexes on frequently queried columns
   - Archive old messages

4. **Load Balancing**
   - Use load balancer for multiple API instances
   - Configure sticky sessions for WebSockets

## Next Steps

1. Test all features in production
2. Set up error tracking (Sentry)
3. Configure email notifications
4. Set up automated backups
5. Monitor performance metrics

## Support

For deployment issues:
1. Check service logs
2. Review environment variables
3. Test API with curl or Postman
4. Check GitHub issues
