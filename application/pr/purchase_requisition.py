from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .prModels import Pr, PrItem
from pydantic import BaseModel
from typing import List
from datetime import datetime, date

# โหลด environment variables
load_dotenv()

# สร้าง SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(os.getenv("DATABASE_URL") or ""))

router = APIRouter()

class PrItemBase(BaseModel):
    pri_id: int
    pri_ref: str
    pri_matname: str
    pri_matcode: str | None = None
    pri_qty: float
    pri_unit: str
    pri_priceunit: float
    pri_amount: float
    pri_discountper1: float | None = None
    pri_discountper2: float | None = None
    pri_discountper3: float | None = None
    pri_discountper4: float | None = None
    pri_discountper5: float | None = None
    pri_discountper6: float | None = None
    pri_discountper7: float | None = None
    pri_discountper8: float | None = None
    pri_discountper9: float | None = None
    pri_discountper10: float | None = None
    pri_discountamt: float | None = None
    pri_sumamt: float | None = None
    pri_boqid: str | None = None
    pri_boqrow: int | None = None
    pri_project: str | None = None
    pri_unitcode: str | None = None
    pri_uniticcode: str | None = None
    cost_type: str | None = None
    remark_mat: str | None = None
    boq_type: str | None = None
    pri_sumqty: str | None = None
    pri_cpqtyic: str | None = None
    pri_pqtyic: str | None = None
    pri_punitic: str | None = None
    pri_pdiscex: int | None = None
    pri_tovat: str | None = None
    pri_boqid: str | None = None
    pri_boqrow: int | None = None
    pri_project: str | None = None

class PrBase(BaseModel):
    pr_prid: int
    pr_item: str | None = None
    pr_prno: str
    pr_prdate: date
    pr_memid: str | None = None
    pr_reqname: str | None = None
    pr_project: str | None = None
    pr_system: str | None = None
    pr_costtype: str | None = None
    pr_department: str | None = None
    pr_vender: str | None = None
    pr_deliplace: str | None = None
    pr_delidate: str | None = None
    pr_status: str | None = None
    pr_remark: str | None = None
    pr_approve: str | None = None
    pe_approve: str | None = None
    pm_approve: str | None = None
    director_approve: str | None = None
    approve_date: date | None = None
    pr_disremark: str | None = None
    po_open: str | None = None
    po_count: str | None = None
    useradd: str | None = None
    usercreate: datetime | None = None
    compcode: str | None = None
    purchase_type: str | None = None
    edituser: str | None = None
    editdate: datetime | None = None
    deluser: str | None = None
    deldate: datetime | None = None
    pono: str | None = None
    wo_open: str | None = None
    express: str | None = None
    reject_remark: str | None = None
    reject_user: str | None = None
    dis_remark: str | None = None
    dis_user: str | None = None
    pri_compare: str | None = None
    compare: str | None = None
    reject_date: datetime | None = None
    subid: str | None = None
    subname: str | None = None
    wo: str | None = None
    is_decrement: str | None = None
    pr_postatus: str | None = None
    items: List[PrItemBase] = []

class PrCreate(PrBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations
@router.post("/pr/", response_model=PrBase)
def create_pr(pr: PrCreate, db: Session = Depends(get_db)):
    try:
        db_pr = Pr(
            pr_prno=pr.pr_prno,
            pr_prdate=pr.pr_prdate,
            pr_memid=pr.pr_memid,
            pr_reqname=pr.pr_reqname,
            pr_project=pr.pr_project,
            pr_system=pr.pr_system,
            pr_costtype=pr.pr_costtype,
            pr_department=pr.pr_department,
            pr_vender=pr.pr_vender,
            pr_deliplace=pr.pr_deliplace,
            pr_delidate=pr.pr_delidate,
            pr_status=pr.pr_status,
            pr_remark=pr.pr_remark,
            pr_approve=pr.pr_approve,
            pe_approve=pr.pe_approve,
            pm_approve=pr.pm_approve,
            director_approve=pr.director_approve,
            approve_date=pr.approve_date,
            pr_disremark=pr.pr_disremark,
            po_open=pr.po_open,
            po_count=pr.po_count,
            useradd=pr.useradd,
            usercreate=pr.usercreate,
            compcode=pr.compcode,
            purchase_type=pr.purchase_type
        )
        db.add(db_pr)
        db.commit()
        db.refresh(db_pr)
        return db_pr
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/pr/{pr_id}", response_model=PrBase)
def read_pr(pr_id: int, db: Session = Depends(get_db)):
    db_pr = db.query(Pr).filter(Pr.pr_prid == pr_id).first()
    if db_pr is None:
        raise HTTPException(status_code=404, detail="PR not found")
    return db_pr

@router.get("/prs/", response_model=List[PrBase])
def read_prs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prs = db.query(Pr).offset(skip).limit(limit).all()
    return prs

@router.put("/pr/{pr_id}", response_model=PrBase)
def update_pr(pr_id: int, pr: PrCreate, db: Session = Depends(get_db)):
    db_pr = db.query(Pr).filter(Pr.pr_prid == pr_id).first()
    if db_pr is None:
        raise HTTPException(status_code=404, detail="PR not found")
    
    for var, value in vars(pr).items():
        setattr(db_pr, var, value)
    
    try:
        db.commit()
        db.refresh(db_pr)
        return db_pr
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/pr/{pr_id}")
def delete_pr(pr_id: int, db: Session = Depends(get_db)):
    db_pr = db.query(Pr).filter(Pr.pr_prid == pr_id).first()
    if db_pr is None:
        raise HTTPException(status_code=404, detail="PR not found")
    
    try:
        db.delete(db_pr)
        db.commit()
        return {"message": "PR deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

