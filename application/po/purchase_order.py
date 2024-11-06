from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import PurchaseOrder, PurchaseOrderItem
from typing import List
from pydantic import BaseModel
from datetime import datetime, date
from fastapi.responses import JSONResponse
from decimal import Decimal  # เพิ่มการนำเข้า Decimal

# โหลด environment variables
load_dotenv()

# สร้าง SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(os.getenv("DATABASE_URL") or ""))

# สร้าง router
router = APIRouter()

# Pydantic models สำหรับ PO Item
class POItemBase(BaseModel):
    poi_id: int
    poi_matname: str
    poi_matcode: str | None = None
    poi_ref: str | None = None 
    poi_costname: str | None = None
    poi_costcode: str | None = None
    poi_qty: float
    poi_unit: str
    poi_priceunit: float
    poi_amount: float
    poi_discountper1: float | None = None
    poi_discountper2: float | None = None
    poid: int

class POItemCreate(POItemBase):
    pass

# Pydantic models สำหรับ PO
class POBase(BaseModel):
    po_id: int
    po_pono: str
    po_podate: date
    po_project: str
    po_system: str | None = None
    po_department: str
    po_memid: str
    po_prname: str | None = None
    po_trem: str | None = None
    po_contact: str | None = None
    po_prno: str | None = None
    po_contactno: str | None = None
    po_quono: str | None = None
    po_deliverydate: date | None = None
    po_place: str | None = None
    po_remark: str | None = None
    po_venderid: int
    po_vender: str
    po_vatper: int | None = None
    items: List[POItemCreate]

class POCreate(POBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
async def create_purchase_order(po: POCreate, db: Session = Depends(get_db)):
    # สร้าง PO
    db_po = PurchaseOrder(
        po_pono=po.po_pono,
        po_podate=po.po_podate,
        po_project=po.po_project,
        po_system=po.po_system,
        po_department=po.po_department,
        po_memid=po.po_memid,
        po_prname=po.po_prname,
        po_trem=po.po_trem,
        po_contact=po.po_contact,
        po_prno=po.po_prno,
        po_contactno=po.po_contactno,
        po_quono=po.po_quono,
        po_deliverydate=po.po_deliverydate,
        po_place=po.po_place,
        po_remark=po.po_remark,
        po_venderid=po.po_venderid,
        po_vender=po.po_vender,
        po_vatper=po.po_vatper,
        usercreate=datetime.now()
    )
    
    db.add(db_po)
    
    try:
        db.commit()
        db.refresh(db_po)
        
        # สร้าง PO Items
        for item in po.items:
            db_item = PurchaseOrderItem(
                poi_matname=item.poi_matname,
                poi_matcode=item.poi_matcode,
                poi_ref=item.poi_ref,
                poi_costname=item.poi_costname,
                poi_costcode=item.poi_costcode,
                poi_qty=item.poi_qty,
                poi_unit=item.poi_unit,
                poi_priceunit=item.poi_priceunit,
                poi_amount=item.poi_amount,
                poi_discountper1=item.poi_discountper1,
                poi_discountper2=item.poi_discountper2,
                poid=db_po.po_id  # เพิ่ม foreign key reference
            )
            db.add(db_item)
            
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{po_id}", response_model=dict)
async def read_purchase_order(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
    if po is None:
        raise HTTPException(status_code=404, detail="ไม่พบ PO")
    
    print(po_id)
    items = db.query(PurchaseOrderItem).filter(PurchaseOrderItem.poid == po_id).all()
    
    return {
        "po_id": po.po_id,
        "po_pono": po.po_pono,
        "po_podate": po.po_podate.isoformat(),
        "po_project": po.po_project,
        "po_system": po.po_system,
        "po_department": po.po_department,
        "po_memid": po.po_memid,
        "po_prname": po.po_prname,
        "po_trem": po.po_trem,
        "po_contact": po.po_contact,
        "po_prno": po.po_prno,
        "po_contactno": po.po_contactno,
        "po_quono": po.po_quono,
        "po_deliverydate": po.po_deliverydate.isoformat(),
        "po_place": po.po_place,
        "po_remark": po.po_remark,
        "po_venderid": po.po_venderid,
        "po_vender": po.po_vender.strip(),
        "po_vatper": po.po_vatper,
        "items": [{
            "poi_id": item.poi_id,
            "poi_matname": item.poi_matname,
            "poi_matcode": item.poi_matcode,
            "poi_ref": item.poi_ref,
            "poi_costname": item.poi_costname,
            "poi_costcode": item.poi_costcode,
            "poi_qty": item.poi_qty,
            "poi_unit": item.poi_unit,
            "poi_priceunit": item.poi_priceunit,
            "poi_amount": item.poi_amount, 
            "poi_discountper1": item.poi_discountper1,
            "poi_discountper2": item.poi_discountper2
        } for item in items]
    }


@router.get("/", response_model=List[dict])
async def read_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pos = db.query(PurchaseOrder).offset(skip).limit(limit).all()
    result = []
    
    for po in pos:
        items = db.query(PurchaseOrderItem).filter(PurchaseOrderItem.poid == po.po_id).all()
        result.append({
            "po_id": po.po_id,
            "po_pono": po.po_pono,
            "po_podate": po.po_podate.isoformat(),
            "po_project": po.po_project,
            "po_vender": po.po_vender.strip(),
            "po_status": po.po_status,
            "po_approve": po.po_approve,
            "items": [{
                "poi_id": item.poi_id,
                "poi_matname": item.poi_matname,
                "poi_matcode": item.poi_matcode,
                "poi_ref": item.poi_ref,
                "poi_costname": item.poi_costname,
                "poi_costcode": item.poi_costcode,
                "poi_qty": item.poi_qty,
                "poi_unit": item.poi_unit,
                "poi_priceunit": item.poi_priceunit,
                "poi_amount": item.poi_amount, 
                "poi_discountper1": item.poi_discountper1,
                "poi_discountper2": item.poi_discountper2
            } for item in items]
        })
    
    return result
