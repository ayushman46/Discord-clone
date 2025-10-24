# 🚀 How to Run the Discord Clone

All services are **already running** and ready to test! Here's what's currently active:

## ✅ Services Status

```
✅ PostgreSQL Database    → localhost:5432
✅ Backend API Server     → http://127.0.0.1:8000
✅ Frontend Dev Server    → http://localhost:5173
```

---

## 🎮 Quick Start (Already Running)

### 1. Open the App in Browser
```
http://localhost:5173
```

### 2. Create an Account
- Click "Register" on the login page
- Fill in:
  - Username (any name)
  - Email (any email format)
  - Password (any password)
- Click "Register"

### 3. Login
- Use the credentials you just created
- Click "Login"

### 4. Create a Server
- Click the "➕ Create Server" button
- Enter a server name (e.g., "My First Server")
- Click "Create"

### 5. Create a Channel
- Click the server you just created
- Click "➕ Add Channel" 
- Enter a channel name (e.g., "general")
- Click "Create"

### 6. Send Your First Message
- Click on the channel
- Type a message in the chat box
- Press Enter or click Send
- Watch it appear in real-time! 🎉

---

## 🧪 Test All Features

### Test Real-Time Messaging
1. Open the app in **two different browser tabs** (or windows)
2. Login with the same account in both
3. Select the same channel in both
4. Send a message from one tab
5. ✅ It should appear instantly in the other tab

### Test Typing Indicator
1. Start typing in the message box
2. A "You are typing..." indicator should appear
3. Stop typing for 3 seconds
4. The indicator should disappear

### Test File Upload
1. In the chat, click the 📎 attachment button
2. Choose an image or document from your computer
3. Click send
4. The file should appear in the chat with a link

### Test Multiple Users (Optional)
1. Open an **incognito/private browser window**
2. Register a **different account**
3. Have both users in the same server/channel
4. Send messages between accounts
5. You'll see who's typing in real-time

### Test the AI Bot
1. In the chat, type: `@bot what is your name?`
2. Or ask: `@bot tell me a fact`
3. The bot should respond with FAQ answers (if properly trained)

---

## 🔧 If Services Stop or You Need to Restart

### Start Backend Server
```bash
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start Frontend Server
```bash
cd /Users/ayush/Downloads/Discord-clone/frontend
npm run dev
```

### Start PostgreSQL (if not running)
```bash
brew services start postgresql@15
```

Or for PostgreSQL 16:
```bash
brew services start postgresql@16
```

### Stop All Services
```bash
# Stop backend: Press Ctrl+C in backend terminal
# Stop frontend: Press Ctrl+C in frontend terminal
# Stop database:
brew services stop postgresql@15
```

---

## 📊 Access Backend API Documentation

### Swagger UI (Interactive)
```
http://127.0.0.1:8000/docs
```

### ReDoc (Clean Documentation)
```
http://127.0.0.1:8000/redoc
```

Here you can:
- See all available endpoints
- Test API calls directly
- View request/response schemas
- Check authentication requirements

---

## 🗂️ Project Structure

```
Discord-clone/
├── backend/                    # FastAPI Python backend
│   ├── main.py                # API endpoints & WebSocket
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic validation
│   ├── database.py            # PostgreSQL connection
│   ├── bot.py                 # AI FAQ bot
│   ├── .env                   # Environment variables (created)
│   ├── requirements.txt        # Python dependencies
│   └── venv/                  # Virtual environment
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── loginpage.tsx
│   │   │   ├── registerpage.tsx
│   │   │   └── mainapppage.tsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── stores/
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── .env                   # Frontend config (created)
│
├── documentation/             # All guides and documentation
├── setup.sh                   # One-command setup script
└── README.md                  # Main project README
```

---

## 🔑 Key Endpoints (API)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create new account |
| POST | `/login` | Login and get JWT token |
| GET | `/me` | Get current user info |
| POST | `/servers` | Create a server |
| GET | `/servers` | List all user's servers |
| POST | `/channels` | Create a channel |
| GET | `/channels/{id}/messages` | Get channel messages |
| POST | `/messages` | Send a message |
| WS | `/ws?token=...` | WebSocket for real-time |
| POST | `/upload` | Upload files |
| POST | `/ask-bot` | Query AI bot |

---

## ⚡ Performance Tips

1. **First Load**: May take 5-10 seconds (FAISS/AI model loading)
2. **Message Sync**: Instant across all connected clients
3. **Typing Indicator**: Updates in real-time with debouncing
4. **File Upload**: Works for any file type, stored locally

---

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 or 5173 is already in use:
```bash
# Find and kill process
lsof -i :8000  # Check port 8000
kill -9 <PID>  # Kill the process

# Or use different ports
# Backend: uvicorn main:app --port 8001
# Frontend: VITE_PORT=5174 npm run dev
```

### Database Connection Error
```bash
# Verify PostgreSQL is running
psql -U postgres -d discord_clone

# If error, restart PostgreSQL
brew services restart postgresql@15
```

### Module Not Found Errors
```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt

# Reinstall frontend dependencies
cd ../frontend
npm install
```

### WebSocket Connection Failed
- Check backend is running: http://127.0.0.1:8000/docs
- Check frontend is on http://localhost:5173 (not 127.0.0.1)
- Check `.env` file has correct `VITE_API_URL=http://127.0.0.1:8000`

---

## 📝 Test Checklist

- [ ] App loads without errors
- [ ] Can register a new account
- [ ] Can login with registered account
- [ ] Can create a server
- [ ] Can create a channel in server
- [ ] Can send a message
- [ ] Message appears in real-time
- [ ] Can upload a file
- [ ] File link appears in chat
- [ ] Typing indicator works
- [ ] Can connect from another tab
- [ ] Messages sync across tabs
- [ ] Bot responds to questions
- [ ] Can disconnect and reconnect

---

## 🎯 What's Implemented

✅ User authentication (JWT)
✅ Server management
✅ Channel management
✅ Real-time messaging (WebSocket)
✅ Typing indicators
✅ User presence (online/offline)
✅ File uploads with storage
✅ AI FAQ bot (FAISS)
✅ Responsive UI (Tailwind CSS)
✅ Type-safe (TypeScript + Python)
✅ CORS enabled for local dev
✅ Auto-reload in development

---

## 🚀 When Ready to Deploy

See **DEPLOYMENT.md** for:
- Production environment setup
- Backend deployment (Render/Railway)
- Frontend deployment (Vercel/Netlify)
- Database setup (Neon/Supabase)
- Environment variables
- Security best practices

---

## 💬 Questions?

Check these files for more information:
- `README.md` - Full project documentation
- `DEPLOYMENT.md` - Deployment instructions
- `PROJECT_SUMMARY.md` - Technical overview
- Backend API Docs: http://127.0.0.1:8000/docs

---

**Happy testing! 🎉**
