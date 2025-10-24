from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime # <-- Added DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # <-- Added this to use func.now()
import database

# This is the "join" table that links Users and Servers
server_members = Table(
    "server_members",
    database.Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("server_id", Integer, ForeignKey("servers.id"), primary_key=True),
)


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    servers = relationship("Server", secondary=server_members, back_populates="members")


class Server(database.Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # --- THIS IS THE NEW LINE ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # --------------------------

    members = relationship("User", secondary=server_members, back_populates="servers")
    channels = relationship("Channel", back_populates="server")


class Channel(database.Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"))

    server = relationship("Server", back_populates="channels")
    messages = relationship("Message", back_populates="channel")


class Message(database.Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    file_url = Column(String, nullable=True)

    channel = relationship("Channel", back_populates="messages")
    owner = relationship("User")