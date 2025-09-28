from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# This is an "association table". It's a special table that doesn't have its
# own model class. Its job is to link Users and Servers together in a
# "many-to-many" relationship (a user can be in many servers, and a
# server can have many users).
server_members = Table(
    "server_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("server_id", Integer, ForeignKey("servers.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # This relationship allows us to easily access all the servers a user is a member of.
    servers = relationship("Server", secondary=server_members, back_populates="members")


class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # This relationship allows us to easily access all the members of a server.
    members = relationship("User", secondary=server_members, back_populates="servers")
    # This relationship allows us to access all channels belonging to this server.
    channels = relationship("Channel", back_populates="server")


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"))

    # This relationship links a channel back to its parent server.
    server = relationship("Server", back_populates="channels")
    # This relationship allows us to access all messages in this channel.
    messages = relationship("Message", back_populates="channel")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # This relationship links a message back to its parent channel.
    channel = relationship("Channel", back_populates="messages")
    # This relationship links a message back to the user who wrote it.
    owner = relationship("User")