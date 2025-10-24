# 🚀 Running Frontend & Backend Simultaneously

## **Option 1: Two Terminal Windows (Recommended for Beginners)**

### Terminal 1: Start the Backend
```bash
cd /Users/ayush/Downloads/Discord-clone/backend

# Run this command
PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/Users/ayush/Downloads/Discord-clone/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
--- Database connection successful! ---
```

✅ Backend is now running at **http://127.0.0.1:8000**

---

### Terminal 2: Start the Frontend
```bash
cd /Users/ayush/Downloads/Discord-clone/frontend

# Run this command
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  press h + enter to show help
```

✅ Frontend is now running at **http://localhost:5173**

---

## **Option 2: One Terminal with Background Process**

If you want to run both from one terminal:

```bash
# Terminal 1: Start Backend
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 &

# Backend runs in background (PID will be printed)
# Example: [1] 12345

# Now start Frontend in same terminal
cd /Users/ayush/Downloads/Discord-clone/frontend
npm run dev

# You'll see Frontend output
# To stop both: Press Ctrl+C in this terminal, then kill the background process
# kill %1  (or kill 12345)
```

---

## **Option 3: Using a Shell Script (Simplest)**

Create a file called `run-all.sh`:

```bash
#!/bin/bash

# Start Backend in background
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Start Frontend in background
cd /Users/ayush/Downloads/Discord-clone/frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "═════════════════════════════════════════════════"
echo "🎉 Both servers running!"
echo "═════════════════════════════════════════════════"
echo ""
echo "🌐 Frontend:  http://localhost:5173"
echo "🔌 Backend:   http://127.0.0.1:8000"
echo "📊 Swagger:   http://127.0.0.1:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "To stop all:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for Ctrl+C
wait
```

Run it:
```bash
chmod +x run-all.sh
./run-all.sh
```

---

## **Option 4: Using npm concurrently (Most Professional)**

1. **Install concurrently in root directory:**
```bash
cd /Users/ayush/Downloads/Discord-clone
npm install concurrently
```

2. **Create or update `package.json` in root:**
```json
{
  "name": "discord-clone",
  "scripts": {
    "dev": "concurrently \"npm run backend\" \"npm run frontend\"",
    "backend": "cd backend && PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000",
    "frontend": "cd frontend && npm run dev"
  },
  "devDependencies": {
    "concurrently": "^8.x.x"
  }
}
```

3. **Run everything with one command:**
```bash
cd /Users/ayush/Downloads/Discord-clone
npm run dev
```

---

## ✅ Quick Verification Checklist

After starting both servers, verify everything is working:

### Backend Check:
```bash
curl http://127.0.0.1:8000/docs
```
- Should load Swagger UI documentation

### Frontend Check:
```bash
curl http://localhost:5173
```
- Should load HTML content

### Both Running Check:
Open browser: **http://localhost:5173**
- Should see login/register page
- If you see it, both are working! ✅

---

## 🛑 How to Stop

### If using Option 1 (Two Terminals):
- **Terminal 1**: Press `Ctrl+C`
- **Terminal 2**: Press `Ctrl+C`

### If using Option 2 (One Terminal):
- Press `Ctrl+C` to stop frontend
- Then run: `kill %1` to stop backend

### If using Option 3 (Shell Script):
- Press `Ctrl+C` in the script terminal
- Or manually: `kill [BACKEND_PID] [FRONTEND_PID]`

### If using Option 4 (npm concurrently):
- Press `Ctrl+C` - stops both automatically

---

## 📝 Common Issues & Solutions

### **Port Already in Use**
```bash
# Kill process on port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Kill process on port 5173
lsof -i :5173 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### **Backend Won't Start - Module Not Found**
```bash
cd /Users/ayush/Downloads/Discord-clone/backend
pip install -r requirements.txt
```

### **Frontend Won't Start - Dependencies Missing**
```bash
cd /Users/ayush/Downloads/Discord-clone/frontend
npm install
```

### **Database Connection Error**
```bash
# Check if PostgreSQL is running
brew services start postgresql@15

# Or start the latest version:
brew services start postgresql@16
```

### **WebSocket Connection Failed**
- Make sure backend is running on `127.0.0.1:8000`
- Make sure frontend is on `localhost:5173` (not 127.0.0.1)
- Check the `.env` file in frontend folder has:
  ```
  VITE_API_URL=http://127.0.0.1:8000
  ```

---

## 🎯 My Recommendation

**Use Option 1 (Two Terminals)** for development because:
- ✅ Easy to see both outputs clearly
- ✅ Easy to stop individual services
- ✅ Easy to troubleshoot issues
- ✅ No additional dependencies needed

Here are the exact commands to copy-paste:

**Terminal 1:**
```bash
cd /Users/ayush/Downloads/Discord-clone/backend && PYTHONPATH=$(pwd) ./venv/bin/python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2:**
```bash
cd /Users/ayush/Downloads/Discord-clone/frontend && npm run dev
```

Then open: **http://localhost:5173** in your browser

---

## 🎉 Once Both Are Running

1. ✅ Open http://localhost:5173 in browser
2. ✅ Register a new account
3. ✅ Create a server and channel
4. ✅ Send messages and see them in real-time
5. ✅ Open frontend in another tab to test sync
6. ✅ Test file uploads and bot responses

---

**Ready to test? Start those terminals! 🚀**
