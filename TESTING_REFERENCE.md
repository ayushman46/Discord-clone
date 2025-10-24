# 📚 Discord Clone - Complete Local Testing Reference

## 🎯 Current Status: READY FOR TESTING ✅

**Backend Server**: http://127.0.0.1:8000 ✅  
**Frontend Server**: http://localhost:5173 ✅  
**Database**: PostgreSQL (localhost:5432) ✅  

---

## 🚀 Quick Links

| Link | Purpose |
|------|---------|
| http://localhost:5173 | **Main App** - Start here! |
| http://127.0.0.1:8000/docs | API Documentation (Swagger) |
| http://127.0.0.1:8000/redoc | API Documentation (ReDoc) |
| LOCAL_TESTING_GUIDE.md | Feature testing checklist |
| TESTING_STATUS.md | Detailed testing instructions |

---

## 🧪 Testing Workflow

### Phase 1: Authentication (5 mins)
```
1. Go to http://localhost:5173
2. Click "Sign Up"
3. Enter: username, email, password
4. Click "Register"
5. Verify: Can login with new account
```

### Phase 2: Server & Channel Creation (5 mins)
```
1. After login, create a server
   - Click "Create Server" button
   - Enter "Test Server"
   - Click Create
2. Create a channel in the server
   - Click "Create Channel"
   - Enter "general"
   - Click Create
3. Verify: Both appear in UI
```

### Phase 3: Real-Time Messaging (10 mins)
```
1. Send a message: "Hello from terminal!"
2. Watch it appear instantly in the chat
3. Verify timestamp and sender info
4. Reload page - message still there? ✅
5. Open in another tab - see message? ✅
```

### Phase 4: Advanced Features (15 mins)
```
1. Test Typing Indicator:
   - Start typing (should show "typing...")
   - Stop typing for 3 seconds (should disappear)
   
2. Test File Upload:
   - Click attachment button
   - Select any file
   - Verify file link appears
   
3. Test Bot:
   - Ask "What is Node.js?"
   - Verify bot responds with FAQ
   
4. Test Multi-User:
   - Open in 2nd browser tab
   - Login differently
   - Send message from tab 1
   - Verify it appears in tab 2 instantly
```

---

## 📊 Feature Verification Matrix

Copy this and mark ✅ as you test each feature:

```
AUTHENTICATION:
  [ ] User registration works
  [ ] User login works
  [ ] JWT token validation works
  [ ] Logout works
  [ ] Session persists on reload

SERVERS & CHANNELS:
  [ ] Can create server
  [ ] Can view servers list
  [ ] Can select server
  [ ] Can create channel in server
  [ ] Can view channels list
  [ ] Can select channel
  [ ] Data persists on reload

MESSAGING:
  [ ] Can send text message
  [ ] Message appears instantly (WebSocket)
  [ ] Message shows sender, timestamp
  [ ] Can see message history on channel load
  [ ] Messages separated by channel
  [ ] Multiple users see same messages

REAL-TIME FEATURES:
  [ ] Typing indicator appears when typing
  [ ] Typing indicator disappears after 3 sec
  [ ] User joined/left notifications work
  [ ] Presence updates in real-time

FILE HANDLING:
  [ ] File upload button works
  [ ] File upload completes
  [ ] File link appears in message
  [ ] Can download/view file

BOT INTEGRATION:
  [ ] Bot accepts questions
  [ ] Bot returns relevant FAQ answers
  [ ] Multiple questions work
  [ ] Response time <3 seconds

PERFORMANCE:
  [ ] Messages <100ms latency
  [ ] No console errors
  [ ] No browser warnings
  [ ] Backend running smoothly
  [ ] Responsive UI on all devices

TOTAL FEATURES WORKING: _____ / 37
```

---

## 🔍 Debugging Guide

### Browser Console Errors (Press F12)

**Error: "WebSocket connection failed"**
```
Solution:
1. Check if backend is running on port 8000
2. Check network tab for WebSocket URL
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try in incognito window
```

**Error: "Cannot fetch from API"**
```
Solution:
1. Verify VITE_API_URL in frontend/.env is correct
2. Check if backend is running
3. Verify CORS is enabled in backend
4. Check browser network tab for actual requests
```

**Error: "Authentication failed"**
```
Solution:
1. Clear localStorage (DevTools > Application > Storage)
2. Register new account
3. Check backend logs for auth errors
```

### Backend Terminal Errors

**"Error loading ASGI app"**
```bash
Solution: Restart backend with PYTHONPATH:
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=/Users/ayush/Downloads/Discord-clone/backend \
/Users/ayush/Downloads/Discord-clone/backend/venv/bin/python3 \
-m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**"Permission denied for table"**
```bash
Solution: Reset database:
dropdb discord_clone
createdb discord_clone
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=/Users/ayush/Downloads/Discord-clone/backend \
/Users/ayush/Downloads/Discord-clone/backend/venv/bin/python3 \
-c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

**"Address already in use"**
```bash
Solution: Kill existing process:
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
# Then restart backend
```

### Database Issues

**Database connection timeout**
```bash
Solution: Check PostgreSQL is running:
brew services list
brew services start postgresql@15

# Verify connection:
psql -U postgres discord_clone
```

---

## 📈 API Testing with Swagger

Visit: **http://127.0.0.1:8000/docs**

### Required Endpoints to Test

#### 1. Authentication
```
POST /auth/register
  Input: {"username": "test", "email": "test@example.com", "password": "Test123!"}
  Expected: Success with user ID

POST /auth/login
  Input: {"username": "test@example.com", "password": "Test123!"}
  Expected: Access token returned
```

#### 2. Servers
```
GET /servers (requires auth)
  Expected: Empty list initially

POST /servers (requires auth)
  Input: {"name": "My Server"}
  Expected: Server created with ID

GET /servers/{server_id}/channels (requires auth)
  Expected: Empty list initially
```

#### 3. Channels
```
POST /servers/{server_id}/channels (requires auth)
  Input: {"name": "general"}
  Expected: Channel created

GET /channels/{channel_id}/messages (requires auth)
  Expected: Empty list initially
```

#### 4. Messages
```
POST /channels/{channel_id}/messages (requires auth)
  Input: {"content": "Hello!"}
  Expected: Message created with timestamp

GET /channels/{channel_id}/messages (requires auth)
  Expected: Returns all messages in channel
```

#### 5. File Upload
```
POST /upload (requires auth, multipart form)
  Input: File to upload
  Expected: File URL returned
```

#### 6. Bot
```
POST /ask-bot (requires auth)
  Input: {"question": "What is React?"}
  Expected: FAQ answer returned
```

---

## 🎯 Test Scenarios

### Scenario 1: Single User Flow (10 mins)
1. Register new user
2. Create server "Personal"
3. Create channel "notes"
4. Send 5 messages
5. Reload page
6. Verify all messages still there ✅

### Scenario 2: Multi-User Chat (15 mins)
1. Open 2 browser tabs
2. Tab 1: Register as "Alice"
3. Tab 2: Register as "Bob"
4. Both join same server and channel
5. Tab 1 sends: "Hello Bob!"
6. Tab 2 sees it immediately ✅
7. Tab 2 sends: "Hi Alice!"
8. Tab 1 sees it immediately ✅

### Scenario 3: File Sharing (10 mins)
1. Create server and channel
2. Click file upload button
3. Upload a test file
4. Verify file link appears in message
5. Download file and verify it's correct ✅

### Scenario 4: Performance Test (15 mins)
1. Send 20 messages rapidly
2. Measure time to see all messages (<1 second)
3. Open DevTools Network tab
4. Verify WebSocket messages <100ms
5. Check no errors in Console ✅

---

## 🚨 Critical Checks Before Deployment

- [ ] All test scenarios pass
- [ ] No console errors (F12 → Console)
- [ ] No backend errors (check terminal)
- [ ] WebSocket connection stable
- [ ] File upload works
- [ ] Bot responds correctly
- [ ] Multiple users can chat
- [ ] Messages persist after reload
- [ ] Performance is acceptable (<100ms)
- [ ] No security warnings

---

## 📝 Checklist for Production Deployment

```
BEFORE DEPLOYING:
  [ ] All local tests pass
  [ ] No console errors
  [ ] Backend performance good
  [ ] Database stable
  [ ] Review DEPLOYMENT.md
  [ ] Test with real domain
  [ ] SSL certificate ready
  [ ] Environment variables documented
  [ ] Backups configured
  [ ] Monitoring setup
  [ ] Error logging enabled
```

---

## 💡 Pro Tips

1. **Use DevTools Network Tab** to watch WebSocket traffic
2. **Check Backend Logs** for actual errors vs frontend issues
3. **Test in Incognito** to avoid cache issues
4. **Use Multiple Browsers** (Chrome, Firefox, Safari) for compatibility
5. **Test on Mobile** for responsive design
6. **Load Test** with many messages to verify performance

---

## 🎯 Success Criteria

✅ **Your app is ready for deployment when:**

1. All 37 features in the matrix work correctly
2. No errors in browser console (F12)
3. No errors in backend terminal
4. WebSocket messages <100ms latency
5. File upload works properly
6. Bot responds within 3 seconds
7. Multiple users can chat simultaneously
8. Messages persist after page reload
9. Performance is smooth and responsive
10. You understand each component and can troubleshoot issues

---

## 🚀 Next: Deployment

Once all tests pass:

1. Read **DEPLOYMENT.md** completely
2. Choose your deployment platform
3. Follow the step-by-step guide
4. Test production deployment
5. Monitor for issues
6. Share with friends! 🎉

---

**Good luck! You've got this! 💪**
