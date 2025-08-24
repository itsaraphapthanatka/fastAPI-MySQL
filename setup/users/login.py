from fastapi import APIRouter, HTTPException, status
from .models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import bcrypt
from .auth import create_access_token

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

class Login(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=dict)
async def login(users: Login):
    with SessionLocal() as db:
        userlogin = db.query(User).filter(User.m_email == users.email).first()
        if not userlogin:
            raise HTTPException(status_code=404, detail={"message": "User not found"})
        
        if not bcrypt.checkpw(users.password.encode('utf-8'), userlogin.m_pass.encode('utf-8')):
            raise HTTPException(status_code=401, detail={"message": "Invalid password"})

        access_token = create_access_token(data={"sub": userlogin.m_email, "user_id": userlogin.m_id})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": userlogin.m_id
        }