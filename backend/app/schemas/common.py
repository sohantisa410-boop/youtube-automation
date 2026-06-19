from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class MessageResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    plan: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ChannelCreate(BaseModel):
    name: str
    niche: str
    uploads_per_day: int = 1
    client_secret_path: str | None = None


class ChannelOut(BaseModel):
    id: int
    user_id: int
    name: str
    niche: str
    uploads_per_day: int
    client_secret_path: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class VideoGenerateRequest(BaseModel):
    channel_id: int
    topic: str


class VideoUploadRequest(BaseModel):
    video_id: int


class VideoOut(BaseModel):
    id: int
    channel_id: int
    title: str
    description: str
    status: str
    video_path: str | None = None
    thumbnail_path: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ScheduleRequest(BaseModel):
    video_id: int
    scheduled_at: datetime


class QueueOut(BaseModel):
    id: int
    video_id: int
    scheduled_at: datetime
    status: str
    retries: int

    model_config = ConfigDict(from_attributes=True)


class UserPlanUpdate(BaseModel):
    plan: Literal["free", "pro"]


class UserStatusUpdate(BaseModel):
    is_active: bool


class ApiKeyCreate(BaseModel):
    provider: str = "internal"


class ApiKeyOut(BaseModel):
    id: int
    provider: str
    key_masked: str

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreateResponse(BaseModel):
    id: int
    provider: str
    key_masked: str
    key_value: str

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummary(BaseModel):
    channels: int
    videos: int
    scheduled: int
    views: int
    likes: int
    comments: int
