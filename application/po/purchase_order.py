from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import PurchaseOrder, PurchaseOrderItem
from ..pr.prModels import PrItem,Pr
from typing import List
from pydantic import BaseModel
from datetime import datetime, date

# โหลด environment variables
load_dotenv()

# สร้าง SessionLocal class
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL",DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DATABASE_URL or ""))

# สร้าง router
router = APIRouter()

# Pydantic models สำหรับ PO Item
class POItemBase(BaseModel):
    poi_matname: str
    poi_matcode: str | None = None
    poi_ref: str | None = None
    poi_costname: str | None = None 
    poi_costcode: str | None = None
    poi_qty: float
    poi_qtyic: str | None = None
    poi_totqtyic: str | None = None
    poi_unitic: str | None = None
    poi_unit: str
    poi_priceunit: float
    poi_amount: float
    poi_discountper1: float | None = None
    poi_discountper2: float | None = None
    poi_disamt: float | None = None
    poi_vat: float | None = None
    poi_vatper: int
    poi_remark: str | None = None
    poi_netamt: float | None = None
    poi_receive: int = 0
    poi_receivetot: int = 0
    po_disex: float = 0.0
    poi_item: int | None = None
    ic_receive: int = 0
    compcode: str | None = None
    pri_id: int | None = None
    poi_chk: str | None = None
    poi_discountper3: float | None = None
    poi_discountper4: float | None = None
    poi_disce: float | None = None
    po_asset: str | None = None
    po_assetid: str | None = None
    po_assetname: str | None = None
    pr_no: str | None = None
    po_boq: str | None = None
    cost_type: str | None = None
    remark_mat: str | None = None
    type_cost: str | None = None
    datesend: str | None = None
    wo_ref: str | None = None
    poi_deduct_status: str | None = None
    poi_sumdeduct: float | None = None
    poi_project: str | None = None
    poid: int

class POItemCreate(POItemBase):
    pass

# Pydantic models สำหรับ PO
class POBase(BaseModel):
    po_poid: int | None = None
    po_pono: str
    po_podate: date
    po_project: str
    po_system: str | None = None
    po_department: str
    po_memid: str
    po_prname: str | None = None
    po_trem: str | None = None
    po_contact: str = ''
    po_prno: str | None = None
    po_contactno: str | None = None
    po_quono: str | None = None
    po_deliverydate: date | None = None
    po_place: str | None = None
    po_remark: str | None = None
    po_status: str = 'enable'
    po_venderid: int
    po_vender: str
    po_open: str = 'no'
    po_approve: str = 'wait'
    po_disapprove: str | None = None
    po_qty: int | None = None
    ic_status: str = 'wait'
    apv_open: str = 'no'
    compcode: str | None = None
    useradd: str | None = None
    usercreate: datetime | None = None
    useredit: str | None = None
    editdate: datetime | None = None
    userdelete: str | None = None
    deletedate: datetime | None = None
    po_vat: float | None = None
    po_vatper: int | None = None
    discounts1: str | None = None
    discounts2: str | None = None
    reject_remark: str | None = None
    reject_user: str | None = None
    dis_remark: str | None = None
    dis_user: str | None = None
    downper: float | None = None
    down: float | None = None
    sumdown: float | None = None
    retentionper: float | None = None
    retention: float | None = None
    sumretention: float | None = None
    status_down: str | None = None
    status_retention: str | None = None
    wo_ref: str | None = None
    poi_deduct_status: str | None = None
    is_decrement: str = 'no'
    contact_store: str | None = None
    teamother: str | None = None
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
    # ตรวจสอบข้อมูลที่จำเป็น
    if not po.po_venderid or not po.po_vender:
        raise HTTPException(status_code=400, detail="กรุณาระบุข้อมูลผู้จำหน่าย")
        
    if not po.items or len(po.items) == 0:
        raise HTTPException(status_code=400, detail="กรุณาระบุรายการสินค้า")
    
    # สร้าง PO
    try:
        po_count = db.query(PurchaseOrder).filter().count()

        db_po = PurchaseOrder(
            po_poid = po_count + 1,
            **po.model_dump(exclude={"items", "po_poid"})
        )
        
        db.add(db_po)
        db.flush() # เพื่อให้ได้ po_id ก่อน commit
        
        # ตรวจสอบ PO
        po_result = db.query(PurchaseOrder).filter(PurchaseOrder.po_pono == po.po_pono).first()
        if po_result is None:
            raise HTTPException(status_code=400, detail="ไม่พบ PO ที่มีหมายเลขนี้")
        po_id = po_result.po_id
        
        # สร้าง PO Items
        for item in po.items:
            if not item.poi_matcode or not item.poi_qty or not item.poi_unit:
                raise HTTPException(status_code=400, detail="ข้อมูลรายการสินค้าไม่ครบถ้วน")
                
            item_dict = item.model_dump()
            item_dict['poid'] = po_id
            db.add(PurchaseOrderItem(**item_dict))

            # อัพเดทสถานะ PR Item
            pr_item = db.query(PrItem).filter(PrItem.pri_id == item.pri_id).first()
            if pr_item:
                pr_item.__setattr__('pri_status', 'open')
                db.add(pr_item)
        db.commit()

        # ตรวจสอบและอัพเดทสถานะ PR
        pr_result = db.query(Pr).filter(Pr.pr_prno == po.po_prno, Pr.compcode == po.compcode).first()
        if not pr_result:
            raise HTTPException(status_code=400, detail="ไม่พบ PR ที่เกี่ยวข้อง")
            
        pri_count = db.query(PrItem).filter(
            PrItem.pri_status == 'open',
            PrItem.pri_ref == po.po_prno,
            PrItem.compcode == po.compcode
        ).count()
        
        pri_count_all = db.query(PrItem).filter(
            PrItem.pri_ref == po.po_prno,
            PrItem.compcode == po.compcode
        ).count()
        
        if pri_count == pri_count_all:
            pr_result.__setattr__('po_open', 'open')
            db.add(po_result)
            
        db.commit()
        db.refresh(po_result)
        
        return {"message": "สร้าง PO สำเร็จ", "po_id": po_id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"เกิดข้อผิดพลาด: {str(e)}")

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
