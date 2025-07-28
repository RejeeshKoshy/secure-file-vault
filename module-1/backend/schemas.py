from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    username: str
    mfa_secret: str | None

    class Config:
        orm_mode = True

class OTPVerify(BaseModel):
    username: str
    otp: str

