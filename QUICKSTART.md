# Quick Start Guide - Discord Clone

Get up and running with Discord Clone in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

## 1. Clone & Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/Discord-clone.git
cd Discord-clone

# Run setup script
# macOS/Linux:
chmod +x setup.sh
./setup.sh

# OR Windows:
setup.bat
```

## 2. Configure Database (1 minute)

```bash
# Start PostgreSQL
# macOS:
brew services start postgresql

# Linux:
sudo systemctl start postgresql

# Create database
createdb discord_clone

# Configure backend/.env
cd backend
cp .env.example .env
# Edit .env and add your database URL:
# DATABASE_URL=postgresql://username:password@localhost:5432/discord_clone
```

## 3. Start Servers (1 minute)

### Option A: Separate Terminals (Recommended)

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or: venv\Scripts\activate on Windows
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Option B: Combined (macOS/Linux)

```bash
npm run dev  # Runs both backend and frontend
```

## 4. Open Application (1 minute)

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 5. Try It Out!

### Register
1. Go to http://localhost:5173/register
2. Create an account
3. Login

### Create Server
1. Click the `+` button in left sidebar
2. Enter server name
3. Click "Create"

### Create Channel
1. Select your server
2. Click "+ Add Channel"
3. Enter channel name
4. Click "Create"

### Send Message
1. Select a channel
2. Type a message
3. Press Enter

### Upload File
1. Click 📎 icon
2. Select a file
3. Message with file link appears

### Use Bot
1. Type in a channel: "@faq-bot How do I create a server?"
2. Get bot response

## Troubleshooting

### Backend won't start
```bash
# Check Python/PostgreSQL
python --version
psql --version

# Check database
psql discord_clone

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules
npm install
npm run dev
```

### WebSocket connection fails
- Check backend is running on port 8000
- Check frontend .env has correct VITE_API_URL
- Check CORS is enabled in backend

### Can't upload files
```bash
# Create uploads directory
mkdir -p backend/uploads
chmod 755 backend/uploads
```

## Next Steps

1. **Read Documentation**
   - README.md - Full feature overview
   - DEPLOYMENT.md - Deploy to production
   - CONTRIBUTING.md - Contribute code

2. **Explore Code**
   - Backend: `backend/main.py` - API and WebSocket
   - Frontend: `frontend/src/pages/mainapppage.tsx` - UI
   - Database: `backend/models.py` - Data schema

3. **Deploy**
   - See DEPLOYMENT.md for Render/Vercel setup

## API Quick Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=pass123"
```

### Get Servers
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/users/me/servers
```

### Get Messages
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/channels/1/messages
```

### Interactive Docs
Visit http://localhost:8000/docs for full API documentation

## File Structure

```
Discord-clone/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── bot.py           # AI bot
│   └── requirements.txt  # Python packages
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom hooks
│   │   └── stores/      # State management
│   └── package.json     # Node packages
├── README.md            # Full documentation
└── DEPLOYMENT.md        # Deploy guide
```

## Important Files

- `.env` - Database connection (backend)
- `.env` - API URL (frontend)
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies

## Getting Help

1. Check README.md
2. Review code comments
3. Check /docs API documentation
4. Open GitHub issues

## Common Commands

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev      # Development
npm run build    # Production build
npm run lint     # Check code style

# Database
createdb discord_clone
psql discord_clone
```

## Tips

- Use browser DevTools for frontend debugging
- Use `/docs` for API testing
- Check server logs for errors
- Test WebSocket in multiple browser tabs

## What's Next?

1. ✅ Get app running locally
2. 📚 Read full README.md
3. 🚀 Deploy to production (see DEPLOYMENT.md)
4. 👥 Invite others
5. 🎓 Explore code and learn

---

**Happy chatting! 🚀**

Questions? Check README.md or open an issue on GitHub.
