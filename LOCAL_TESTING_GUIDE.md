# 🧪 Local Testing Guide

Your Discord Clone is now running locally! Here's how to test all the features before deployment.

## ✅ Prerequisites Verified
- ✅ PostgreSQL database created and running
- ✅ Backend server running on `http://127.0.0.1:8000`
- ✅ Frontend development server running on `http://localhost:5173`

## 🚀 Testing Flow

### 1. **Register a New User**
   - Go to `http://localhost:5173`
   - Click "Sign Up" if you see the auth page
   - Fill in username, email, and password
   - Click "Register"
   - Expected: You're redirected to the main app or login page

### 2. **Login with Your Credentials**
   - If not automatically logged in, login with your credentials
   - Expected: You see the main chat interface with an empty server list

### 3. **Create a Server**
   - Look for a "Create Server" button or input field
   - Enter a server name (e.g., "My Test Server")
   - Click "Create"
   - Expected: Server appears in the left sidebar

### 4. **Create a Channel**
   - Select the server you just created
   - Look for "Create Channel" button
   - Enter a channel name (e.g., "general")
   - Click "Create"
   - Expected: Channel appears in the channel list

### 5. **Send a Message**
   - Click on the channel you created
   - Type a message in the message input box
   - Click "Send" or press Enter
   - Expected: Message appears in the chat with timestamp, sender name, and your avatar

### 6. **Test Real-time Messaging**
   - Open the app in another browser tab or window (same or different login)
   - Send a message from tab 1
   - Expected: Message appears instantly in tab 2 without refresh

### 7. **Test Typing Indicator**
   - Start typing in the message input
   - Expected: See "User is typing..." indicator in chat (or similar)
   - Stop typing for 3 seconds
   - Expected: Typing indicator disappears

### 8. **Test File Upload**
   - Click the file/attachment icon in the message input area
   - Select a file from your computer
   - Expected: File is uploaded and appears as a link in the message

### 9. **Test User Presence**
   - Send a message in one tab
   - Open another browser tab/window and login
   - Expected: See notifications like "User joined" in the chat

### 10. **Test the FAQ Bot**
   - Look for a "Bot" or "FAQ" input field
   - Ask a question like "What is React?" or "How do I use WebSockets?"
   - Expected: Bot returns a relevant FAQ answer from the knowledge base

## 🔍 API Testing (Advanced)

### Test Endpoints with Swagger UI
Visit: `http://127.0.0.1:8000/docs`

Key endpoints to test:
- **POST /auth/register** - Create a new user
- **POST /auth/login** - Login and get JWT token
- **GET /servers** - List your servers
- **POST /servers** - Create new server
- **GET /servers/{server_id}/channels** - List channels in server
- **POST /servers/{server_id}/channels** - Create new channel
- **GET /channels/{channel_id}/messages** - Get message history
- **POST /channels/{channel_id}/messages** - Send message
- **POST /upload** - Upload a file
- **POST /ask-bot** - Query the FAQ bot

### WebSocket Testing
Connect to: `ws://127.0.0.1:8000/ws?token=YOUR_JWT_TOKEN`

Send messages with this format:
```json
{
  "type": "message",
  "channel_id": 1,
  "content": "Hello, World!"
}
```

Or typing indicator:
```json
{
  "type": "typing",
  "channel_id": 1
}
```

## 📊 Expected Performance
- Messages should appear in <100ms
- File uploads should complete within 2-5 seconds
- Bot responses within 1-2 seconds
- No console errors in browser DevTools

## ⚠️ Troubleshooting

### Issue: Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process
kill -9 <PID>

# Restart:
cd /Users/ayush/Downloads/Discord-clone/backend
PYTHONPATH=/Users/ayush/Downloads/Discord-clone/backend \
/Users/ayush/Downloads/Discord-clone/backend/venv/bin/python3 \
-m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Issue: Frontend won't load
```bash
# Check if port 5173 is in use
lsof -i :5173

# Restart:
cd /Users/ayush/Downloads/Discord-clone/frontend
npx vite
```

### Issue: WebSocket connection fails
- Check browser console for errors
- Verify backend is running
- Clear browser cache and cookies
- Try in an incognito/private window

### Issue: Database errors
- Verify PostgreSQL is running: `brew services list`
- Check .env file has correct DATABASE_URL
- Try recreating tables: `python3 setup_db.py` in backend directory

## 📝 Test Checklist

- [ ] User Registration works
- [ ] User Login works
- [ ] Create Server works
- [ ] Create Channel works
- [ ] Send Message works
- [ ] Receive Messages in real-time (WebSocket)
- [ ] Typing Indicator appears
- [ ] Typing Indicator disappears
- [ ] File Upload works
- [ ] File Link appears in message
- [ ] User Presence notifications work
- [ ] Bot responds to questions
- [ ] No console errors in browser
- [ ] No errors in backend terminal
- [ ] Database queries are fast (<100ms)

## 🎯 Next Steps

Once all tests pass:
1. Review the DEPLOYMENT.md guide
2. Test with additional users (create multiple accounts)
3. Test on mobile if possible
4. Check performance with Network tab in DevTools
5. Review security settings and secrets
6. Deploy to production!

## 📚 Documentation Files

- **QUICKSTART.md** - Quick setup guide (you just completed this!)
- **DEPLOYMENT.md** - Production deployment guide
- **API_ENDPOINTS.md** - Full API documentation
- **ARCHITECTURE.md** - Technical architecture overview

---

**Happy Testing! 🚀**
