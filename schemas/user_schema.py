from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        description="Unique username, at least 3 characters"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Plain-text password, at least 6 characters"
    )
    device_id: str = Field(
        ...,
        min_length=1,
        description="Unique device identifier (string)"
    )

class UserRead(BaseModel):
    user_id:   int
    username:  str
    device_id: str

    class Config:
        orm_mode = True
