from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload # <-- Import joinedload
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
import bcrypt
import json
import shutil
from pathlib import Path

# Use absolute imports
import models
import schemas
import database
import bot as bot_module

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Try to serve static files from uploads directory
try:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except Exception:
    pass  # Will handle if StaticFiles is unavailable

# --- CORS MIDDLEWARE ---
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Connection Manager for WebSockets ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}  # Map user_id to websocket
        self.typing_users: set[int] = set()

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        self.typing_users.discard(user_id)

    async def broadcast(self, payload: dict, exclude_user: int | None = None):
        message_str = json.dumps(payload)
        disconnected_users = []
        for user_id, connection in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await connection.send_text(message_str)
            except Exception:
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)

    async def send_personal(self, user_id: int, payload: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(payload))
            except Exception:
                self.disconnect(user_id)

channel_managers: dict[int, ConnectionManager] = {}

# --- Security & Hashing ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user_from_token(token: str, db: Session): # Removed Depends() for reuse in WebSocket
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: return None
    except JWTError:
        return None
    return db.query(models.User).filter(models.User.email == email).first()

async def get_current_user_from_header(authorization: str = None, db: Session = Depends(get_db)) -> models.User:
    """Extract token from Authorization header and return current user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ")[1]
    user = await get_current_user_from_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# --- UPDATED Message History Endpoint ---
@app.get("/channels/{channel_id}/messages", response_model=list[schemas.Message])
def get_channel_messages(channel_id: int, db: Session = Depends(get_db)):
    # FIXED: Use a JOIN to fetch users and messages in a single query
    messages = (
        db.query(models.Message)
        .options(joinedload(models.Message.owner)) # This performs the JOIN
        .filter(models.Message.channel_id == channel_id)
        .order_by(models.Message.id.asc())
        .limit(50)
        .all()
    )
    return messages

# --- NEW: User Endpoints ---
@app.get("/users/me", response_model=schemas.User)
def get_current_user_info(authorization: str = None, db: Session = Depends(get_db)):
    """Get current authenticated user information"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user

@app.get("/users/me/servers", response_model=list[schemas.Server])
def get_user_servers(authorization: str = None, db: Session = Depends(get_db)):
    """Get all servers the current user belongs to"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Return servers where user is a member or owner
    servers = (
        db.query(models.Server)
        .outerjoin(models.server_members)
        .filter((models.server_members.c.user_id == user.id) | (models.Server.owner_id == user.id))
        .distinct()
        .all()
    )
    return servers

# --- NEW: Server Endpoints ---
@app.post("/servers", response_model=schemas.Server, status_code=status.HTTP_201_CREATED)
def create_server(server_data: schemas.ServerCreate, authorization: str = None, db: Session = Depends(get_db)):
    """Create a new server (current user becomes owner)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    new_server = models.Server(name=server_data.name, owner_id=user.id)
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@app.get("/servers/{server_id}/channels", response_model=list[schemas.Channel])
def get_server_channels(server_id: int, db: Session = Depends(get_db)):
    """Get all channels in a server"""
    channels = db.query(models.Channel).filter(models.Channel.server_id == server_id).all()
    if not channels and not db.query(models.Server).filter(models.Server.id == server_id).first():
        raise HTTPException(status_code=404, detail="Server not found")
    return channels

@app.post("/servers/{server_id}/channels", response_model=schemas.Channel, status_code=status.HTTP_201_CREATED)
def create_channel(server_id: int, channel_data: schemas.ChannelCreate, authorization: str = None, db: Session = Depends(get_db)):
    """Create a new channel in a server"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Check if server exists and user is owner
    server = db.query(models.Server).filter(models.Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    if server.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Only server owner can create channels")
    
    new_channel = models.Channel(name=channel_data.name, server_id=server_id)
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel

@app.post("/channels/{channel_id}/upload", status_code=status.HTTP_200_OK)
async def upload_file(channel_id: int, file: UploadFile = File(...), authorization: str = None, db: Session = Depends(get_db)):
    """Upload a file to a channel"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Verify channel exists
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Save file
    file_path = UPLOAD_DIR / f"{channel_id}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"file_url": f"/uploads/{file_path.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

# --- UPDATED WebSocket Endpoint ---
@app.websocket("/ws/{channel_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: int, token: str = Query(...)):
    # Use a context manager for the database session
    with database.SessionLocal() as db:
        user = await get_current_user_from_token(token=token, db=db)
    
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    if channel_id not in channel_managers:
        channel_managers[channel_id] = ConnectionManager()
    manager = channel_managers[channel_id]

    await manager.connect(websocket, user.id)

    # Announce user joined
    connect_message = {
        "type": "user_joined",
        "username": "System",
        "content": f"{user.username} has joined the chat.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await manager.broadcast(connect_message)

    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                # If not JSON, treat as regular message
                message_data = {"type": "message", "content": data}
            
            msg_type = message_data.get("type", "message")
            
            if msg_type == "typing":
                # Broadcast typing indicator to other users
                typing_message = {
                    "type": "typing",
                    "username": user.username,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                await manager.broadcast(typing_message, exclude_user=user.id)
                
            elif msg_type == "message":
                content = message_data.get("content", "")
                file_url = message_data.get("file_url")
                
                # Save message to database
                with database.SessionLocal() as db:
                    new_message = models.Message(
                        content=content, 
                        channel_id=channel_id, 
                        owner_id=user.id,
                        file_url=file_url,
                        timestamp=datetime.now(timezone.utc)
                    )
                    db.add(new_message)
                    db.commit()
                    db.refresh(new_message)

                # Broadcast message
                message_obj = {
                    "type": "message",
                    "id": new_message.id,
                    "username": user.username,
                    "content": content,
                    "file_url": file_url,
                    "timestamp": new_message.timestamp.isoformat() if new_message.timestamp else datetime.now(timezone.utc).isoformat()
                }
                await manager.broadcast(message_obj)
            
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        disconnect_message = {
            "type": "user_left",
            "username": "System",
            "content": f"{user.username} has left the chat.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await manager.broadcast(disconnect_message)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(user.id)

# ... (rest of your hashing functions and HTTP endpoints are unchanged) ...
def get_password_hash(password: str) -> str:
    pwd = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8')[:72],
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Discord Clone API"}

@app.post("/register/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Bot Endpoints ---
@app.post("/ask-bot")
def ask_bot_endpoint(question: dict, authorization: str = None, db: Session = Depends(get_db)):
    """Ask the FAQ bot a question"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email:
            user = db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        pass
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    question_text = question.get("question", "")
    if not question_text:
        raise HTTPException(status_code=400, detail="Question is required")
    
    try:
        bot = bot_module.get_bot()
        answer = bot.ask(question_text)
        
        if answer:
            return {"answer": answer, "found": True}
        else:
            return {"answer": "I don't have an answer to that question. Please try asking something else.", "found": False}
    except Exception as e:
        print(f"Bot error: {e}")
        return {"answer": "Sorry, I encountered an error. Please try again.", "found": False}

def init_db(db: Session):
    server = db.query(models.Server).first()
    if not server:
        default_server = models.Server(name="Main Server", owner_id=1) # Assuming a first user exists or handle this case
        db.add(default_server)
        db.commit()
            
        default_channel = models.Channel(name="general", server_id=default_server.id)
        db.add(default_channel)
        db.commit()

# Initialize bot on startup
try:
    bot_module.initialize_bot()
except Exception as e:
    print(f"Warning: Could not initialize bot: {e}")

# Run init_db only if this file is executed directly (for setup), not by uvicorn
if __name__ == "__main__":
    with database.SessionLocal() as db:
        init_db(db)