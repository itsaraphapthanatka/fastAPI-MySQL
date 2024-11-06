from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import User
from typing import List
from pydantic import BaseModel
from datetime import datetime

# โหลด environment variables
load_dotenv()

# สร้าง SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(os.getenv("DATABASE_URL") or ""))

# สร้าง router
router = APIRouter()

# Pydantic models
class UserBase(BaseModel):
    m_code: str
    m_firstname: str
    m_lastname: str
    m_user: str
    m_pass: str
    m_email: str
    m_position: str
    m_department: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    m_firstname: str | None = None
    m_lastname: str | None = None
    m_email: str | None = None
    m_position: str | None = None
    m_department: str | None = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        m_code=user.m_code,
        m_firstname=user.m_firstname,
        m_lastname=user.m_lastname,
        m_user=user.m_user,
        m_pass=user.m_pass,
        m_email=user.m_email,
        m_position=user.m_position,
        m_department=user.m_department
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return {"message": "สร้างผู้ใช้สำเร็จ", "user_id": db_user.m_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=dict)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.m_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ไม่พบผู้ใช้")
    return {
        "m_id": user.m_id,
        "m_code": user.m_code,
        "m_firstname": user.m_firstname,
        "m_lastname": user.m_lastname,
        "m_email": user.m_email,
        "m_position": user.m_position,
        "m_department": user.m_department
    }

@router.get("/", response_model=List[dict])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [{
        "m_id": user.m_id,
        "m_code": user.m_code,
        "m_firstname": user.m_firstname,
        "m_lastname": user.m_lastname,
        "m_email": user.m_email,
        "m_position": user.m_position,
        "m_department": user.m_department
    } for user in users]

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.m_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="ไม่พบผู้ใช้")
    
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    try:
        db.commit()
        return {"message": "อัพเดทข้อมูลผู้ใช้สำเร็จ"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.m_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ไม่พบผู้ใช้")
    
    try:
        db.delete(user)
        db.commit()
        return {"message": "ลบผู้ใช้สำเร็จ"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
