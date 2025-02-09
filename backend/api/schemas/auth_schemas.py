from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, UUID4, constr


class UserCreate(BaseModel):
    name: constr(min_length=3, max_length=50) = Field(..., description="Name of the user")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password for the user (8-128 characters)"
    )
    email: str | None = None


class UserDB(UserCreate):
    id: int
    created_at: datetime = Field(default_factory=datetime.now, description="User creation timestamp")

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")


class TokenPayload(BaseModel):
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp of the token")


class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserOutList(BaseModel):
    id: int
    name: str
    email: str | None = None
    hashed_password: str

    class Config:
        orm_mode = True
