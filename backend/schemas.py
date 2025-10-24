from pydantic import BaseModel, ConfigDict
from datetime import datetime

# This is a schema for the User, used for nesting in the Message schema
class User(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Message(BaseModel):
    id: int
    content: str
    owner: User # This will nest the User's info inside the message
    timestamp: datetime | None = None
    file_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Channel(BaseModel):
    id: int
    name: str
    server_id: int

    model_config = ConfigDict(from_attributes=True)


class ChannelCreate(BaseModel):
    name: str


class Server(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ServerCreate(BaseModel):
    name: str


class ServerWithChannels(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime | None = None
    channels: list[Channel] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None