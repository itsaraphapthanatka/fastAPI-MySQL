from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import Project
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
class ProjectBase(BaseModel):
    project_code: str
    project_name: str
    project_worktype: str
    project_type: str
    project_address: str | None = None
    project_cname: str | None = None
    project_tel: str | None = None
    project_email: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_name: str | None = None
    project_worktype: str | None = None
    project_type: str | None = None
    project_address: str | None = None
    project_cname: str | None = None
    project_tel: str | None = None
    project_email: str | None = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(
        project_code=project.project_code,
        project_name=project.project_name,
        project_worktype=project.project_worktype,
        project_type=project.project_type,
        project_address=project.project_address,
        project_cname=project.project_cname,
        project_tel=project.project_tel,
        project_email=project.project_email
    )
    db.add(db_project)
    try:
        db.commit()
        db.refresh(db_project)
        return {"message": "สร้างโครงการสำเร็จ", "project_id": db_project.project_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}", response_model=dict)
async def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="ไม่พบโครงการ")
    return {
        "project_id": project.project_id,
        "project_code": project.project_code,
        "project_name": project.project_name,
        "project_worktype": project.project_worktype,
        "project_type": project.project_type,
        "project_address": project.project_address,
        "project_cname": project.project_cname,
        "project_tel": project.project_tel,
        "project_email": project.project_email
    }

@router.get("/", response_model=List[dict])
async def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return [{
        "project_id": project.project_id,
        "project_code": project.project_code,
        "project_name": project.project_name,
        "project_worktype": project.project_worktype,
        "project_type": project.project_type,
        "project_address": project.project_address,
        "project_cname": project.project_cname,
        "project_tel": project.project_tel,
        "project_email": project.project_email
    } for project in projects]

@router.put("/{project_id}", response_model=dict)
async def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.project_id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="ไม่พบโครงการ")
    
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    try:
        db.commit()
        return {"message": "อัพเดทข้อมูลโครงการสำเร็จ"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}", response_model=dict)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="ไม่พบโครงการ")
    
    try:
        db.delete(project)
        db.commit()
        return {"message": "ลบโครงการสำเร็จ"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

