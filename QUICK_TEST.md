# 🚀 Quick Reference - Discord Clone Local Testing

## ✅ Current Status: READY TO TEST

```
✅ Backend:  http://127.0.0.1:8000        (FastAPI running)
✅ Frontend: http://localhost:5173         (React/Vite running)
✅ Database: PostgreSQL on localhost:5432  (discord_clone database)
```

---

## 🎯 Start Testing NOW!

### Step 1: Open the App
```
http://localhost:5173
```

### Step 2: Register
- Username, Email, Password
- Click Register

### Step 3: Create Server + Channel
- "Create Server" button
- "Create Channel" in the server

### Step 4: Send Messages
- Type message → Press Enter
- Watch it appear instantly (WebSocket)
- Open another tab → Messages sync!

### Step 5: Test Features
- **Typing**: Start typing (should show "typing...")
- **Files**: Click attachment button, upload file
- **Bot**: Ask a question, bot responds
- **Presence**: Open another tab, see "user joined"

---

## 📚 Documentation Files

| File | Read When |
|------|-----------|
| **LOCAL_TESTING_GUIDE.md** | Quick 10-feature test (5-10 mins) |
| **TESTING_STATUS.md** | Detailed testing with checklist (30+ mins) |
| **TESTING_REFERENCE.md** | Complete reference guide (comprehensive) |
| **DEPLOYMENT.md** | After testing passes (ready to deploy) |

---

## 🔗 Useful Links

```
App:               http://localhost:5173
API Docs:          http://127.0.0.1:8000/docs
API (Alternate):   http://127.0.0.1:8000/redoc
WebSocket:         ws://127.0.0.1:8000/ws?token=YOUR_TOKEN
```

---

## 🛠️ Server Commands

### Backend
```bash
# Already running! But to restart:
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=/Users/ayush/Downloads/Discord-clone/backend \
/Users/ayush/Downloads/Discord-clone/backend/venv/bin/python3 \
-m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend
```bash
# Already running! But to restart:
cd /Users/ayush/Downloads/Discord-clone/frontend
npx vite
```

### Stop Everything
- Backend: Ctrl+C in backend terminal
- Frontend: Ctrl+C in frontend terminal
- Database: `brew services stop postgresql@15`

---

## 🧪 Quick Test Checklist

Copy and paste to track your testing:

```
AUTHENTICATION:
☐ Register new user
☐ Login with credentials
☐ Session persists on reload

SERVERS & CHANNELS:
☐ Create server
☐ Create channel
☐ Both appear in UI

MESSAGING:
☐ Send message
☐ Message appears instantly
☐ Has sender, timestamp
☐ Open in 2nd tab - message syncs?

FEATURES:
☐ Typing indicator works
☐ File upload works
☐ Bot responds to questions
☐ User presence notifications appear

PERFORMANCE:
☐ No console errors (F12)
☐ Messages <100ms latency
☐ Responsive UI

STATUS: ____/15 passed
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't access http://localhost:5173 | Frontend not running. Restart with `npx vite` |
| Can't access http://127.0.0.1:8000/docs | Backend not running. Check terminal output |
| WebSocket connection fails | Check browser console (F12) and network tab |
| Database errors | Run: `dropdb discord_clone && createdb discord_clone` |
| Port 8000/5173 in use | Kill process: `lsof -i :8000` then `kill -9 PID` |

---

## 📈 Success Criteria

Your app is ready to deploy when:
- ✅ All 15 items in checklist pass
- ✅ No console errors
- ✅ Real-time messages work
- ✅ File upload works
- ✅ Bot responds
- ✅ Multiple users can chat

---

## 🎉 Next Steps

1. **Run through tests** (30-60 mins)
2. **Read DEPLOYMENT.md** 
3. **Deploy to production**
4. **Tell your friends!** 🚀

---

## 💡 Pro Tips

- Use **F12** in browser to check console for errors
- Watch **Network tab** (F12) to verify WebSocket connection
- Keep **backend terminal** visible to spot errors
- Test on **multiple browsers** (Chrome, Firefox, Safari)
- Test on **mobile** for responsive design

---

**Ready? Open http://localhost:5173 and start testing!**
