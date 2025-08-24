from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import Company
from typing import List
from pydantic import BaseModel
from datetime import date,datetime
from ..users.auth import verify_token
from typing import Optional

# โหลด environment variables
load_dotenv()
# สร้าง SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(os.getenv("DATABASE_URL") or ""))
# สร้าง router
router = APIRouter()
# Pydantic models
class CompanyBase(BaseModel):
    company_code: str | None = None
    company_taxnum: str | None = None
    company_name: str | None = None
    company_address: str | None = None
    company_tel: str | None = None
    company_fax: str | None = None
    company_email: str | None = None
    company_contact: str | None = None
    comp_img: str | None = None
    compcode: str | None = None
    ic_type: str | None = 'fifo'
    start_accost: str | None = None
    end_accost: str | None = None
    startrev: str | None = None
    endrev: str | None = None
    glrap: str | None = None
    startexp: str | None = None
    endexp: str | None = None
    acdate: date | None = None  # Changed from date to string for Pydantic compatibility
    chkvat: str | None = None
    glrar: str | None = None
    dptandproj: str | None = None
    useradd: str | None = None
    createdate: datetime | None = None  # Changed from datetime to string for Pydantic compatibility
    useredit: str | None = None
    editdate: datetime | None = None  # Changed from datetime to string for Pydantic compatibility
    userdel: str | None = None
    deldate: datetime | None = None  # Changed from datetime to string for Pydantic compatibility
    updatetime: str | None = None  # Changed from datetime to string for Pydantic compatibility
    company_nameth: str | None = None
    company_add_en: str | None = None
    company_address2: str | None = None
    company_address3: str | None = None
    company_add_en2: str | None = None
    company_add_en3: str | None = None
    company_telen: str | None = None
    company_faxen: str | None = None
    company_emailen: str | None = None
    company_contacten: str | None = None
    compcodeen: str | None = None
    company_taxnumen: str | None = None
    site_url: str | None = None
    auto_post_gl: str | None = None
    wt_tax: str | None = None
    wt_taxen: int | None = None

class CompanyCreate(CompanyBase):
    pass
class CompanyUpdate(BaseModel):
    company_code: str | None = None
    company_taxnum: str | None = None
    company_name: str | None = None
    company_address: str | None = None
    company_tel: str | None = None
    company_fax: str | None = None
    company_email: str | None = None
    company_contact: str | None = None
    comp_img: str | None = None
    compcode: str | None = None
    ic_type: str | None = None
    start_accost: str | None = None
    end_accost: str | None = None
    startrev: str | None = None
    endrev: str | None = None
    glrap: str | None = None
    startexp: str | None = None
    endexp: str | None = None
    acdate: str | None = None  # Changed from date to string for Pydantic compatibility
    chkvat: str | None = None
    glrar: str | None = None
    dptandproj: str | None = None
    useradd: str | None = None
    createdate: str | None = None  # Changed from datetime to string for Pydantic compatibility
    useredit: str | None = None
    editdate: str | None = None  # Changed from datetime to string for Pydantic compatibility
    userdel: str | None = None
    deldate: str | None = None  # Changed from datetime to string for Pydantic compatibility
    updatetime: str | None = None  # Changed from datetime to string for Pydantic compatibility
    company_nameth: str | None = None
    company_add_en: str | None = None
    company_address2: str | None = None
    company_address3: str | None = None
    company_add_en2: str | None = None
    company_add_en3: str | None = None
    company_telen: str | None = None
    company_faxen: str | None = None
    company_emailen: str | None = None
    company_contacten: str | None = None
    compcodeen: str | None = None
    company_taxnumen: str | None
    site_url: str | None = None
    auto_post_gl: str | None = None
    wt_tax: str | None = None

class PageFilter(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 50

class CompanyFilter(BaseModel):
    search: Optional[str]
    page: PageFilter = PageFilter()

class CompanyListResponse(BaseModel):
    resultLists: List[CompanyBase]
    totalRecords: int
    currentPage: int
    recordsPerPage: int
    totalPage: int
    recordStart: int
    recordEnd: int
    status: str
    

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):    
    db_company = Company(
        company_code=company.company_code,
        company_taxnum=company.company_taxnum,
        company_name=company.company_name,
        company_address=company.company_address,
        company_tel=company.company_tel,
        company_fax=company.company_fax,
        company_email=company.company_email,
        company_contact=company.company_contact,
        comp_img=company.comp_img,
        compcode=company.compcode,
        ic_type=company.ic_type,
        start_accost=company.start_accost,
        end_accost=company.end_accost,
        startrev=company.startrev,
        endrev=company.endrev,
        glrap=company.glrap,
        startexp=company.startexp,
        endexp=company.endexp,
        acdate=company.acdate,
        chkvat=company.chkvat,
        glrar=company.glrar,
        dptandproj=company.dptandproj,
        useradd=company.useradd,
        createdate=company.createdate,
        useredit=company.useredit,
        editdate=company.editdate,
        userdel=company.userdel,
        deldate=company.deldate,
        updatetime=company.updatetime,
        company_nameth=company.company_nameth,
        company_add_en=company.company_add_en,
        company_address2=company.company_address2,
        company_address3=company.company_address3,
        company_add_en2=company.company_add_en2,
        company_add_en3=company.company_add_en3,
        company_telen=company.company_telen,
        company_faxen=company.company_faxen,
        company_emailen=company.company_emailen,
        company_contacten=company.company_contacten,
        compcodeen=company.compcodeen,
        company_taxnumen=company.company_taxnumen,
        site_url=company.site_url,
        auto_post_gl=company.auto_post_gl,
        wt_tax=company.wt_tax,
        wt_taxen=company.wt_taxen
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return {"message": "Company created successfully", "company_id": db_company.company_id}

@router.post("/companies/filter", response_model=CompanyListResponse)
async def filter_companies(filter: CompanyFilter, db: Session = Depends(get_db)):    
    query = db.query(Company)
    if filter.search :
        query = query.filter(Company.company_name.ilike(f"%{filter.search}%"))

    # print(query)
    total_count = query.count()

    limit = filter.page.limit or 50
    page = filter.page.skip or 0

    offset = (page - 1) * limit

    
    companies = query.offset(page).limit(limit).all()
    total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)
    recordStart = offset + 1 if total_count > 0 else 0
    recordEnd = min(offset + limit, total_count)    
    return {
        "resultLists": [
            {   
                "company_id": company.company_id,
                "company_code": company.company_code,
                "company_taxnum": company.company_taxnum,
                "company_name": company.company_name,
                "company_address": company.company_address,
                "company_tel": company.company_tel,
                "company_fax": company.company_fax,
                "company_email": company.company_email,
                "company_contact": company.company_contact,
                "comp_img": company.comp_img,
                "compcode": company.compcode,
                "ic_type": company.ic_type,
                "start_accost": company.start_accost,
                "end_accost": company.end_accost,
                "startrev": company.startrev,
                "endrev": company.endrev,
                "glrap": company.glrap,
                "startexp": company.startexp,
                "endexp": company.endexp,
                "acdate": company.acdate,
                "chkvat": company.chkvat,
            } for company in companies
        ],
        "totalRecords": total_count,
        "currentPage": page,
        "recordsPerPage": limit,
        "totalPage": total_pages,
        "recordStart": recordStart,
        "recordEnd": recordEnd,
        "status": "success"
    }

# @router.get("/", response_model=CompanyListResponse)
# async def read_companies(search: str = "" , skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):    
#     companies = db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).offset(skip).limit(limit).all()
#     print(companies)
#     return {
#         "resultLists": [
#             {   
#                 "company_id": company.company_id,
#                 "company_code": company.company_code,
#                 "company_taxnum": company.company_taxnum,
#                 "company_name": company.company_name,
#                 "company_address": company.company_address,
#                 "company_tel": company.company_tel,
#                 "company_fax": company.company_fax,
#                 "company_email": company.company_email,
#                 "company_contact": company.company_contact,
#                 "comp_img": company.comp_img,
#                 "compcode": company.compcode,
#                 "ic_type": company.ic_type,
#                 "start_accost": company.start_accost,
#                 "end_accost": company.end_accost,
#                 "startrev": company.startrev,
#                 "endrev": company.endrev,
#                 "glrap": company.glrap,
#                 "startexp": company.startexp,
#                 "endexp": company.endexp,
#                 "acdate": company.acdate,
#                 "chkvat": company.chkvat,
#             } for company in companies
#         ],
#         "totalRecords": db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).count(),
#         "currentPage": (skip // limit) + 1,
#         "recordsPerPage": limit,
#         "totalPage": (db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).count() // limit) + (1 if db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).count() % limit > 0 else 0),
#         "recordStart": skip + 1 if db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).count() > 0 else 0,
#         "recordEnd": min(skip + limit, db.query(Company).filter(Company.company_name.ilike(f"%{search}%")).count()),
#         "status": "success"
#     }

@router.get("/{company_id}", response_model=dict)
async def read_company(company_id: int, db: Session = Depends(get_db)):    
    db_company = db.query(Company).filter(Company.company_id == company_id).first()
    print(db_company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db_company_count = db.query(Company).count()
    total_pages = (db_company_count // 10) + (1 if db_company_count % 10 > 0 else 0)  # Assuming 10 records per page
    result_dict = {
        "resultLists": [
            {
                "company_id": db_company.company_id,
                "company_code": db_company.company_code,
                "company_taxnum": db_company.company_taxnum,
                "company_name": db_company.company_name,
                "company_address": db_company.company_address,
                "company_tel": db_company.company_tel,
                "company_fax": db_company.company_fax,
                "company_email": db_company.company_email,
                "company_contact": db_company.company_contact,
                "comp_img": db_company.comp_img,
                "compcode": db_company.compcode,
                "ic_type": db_company.ic_type,
                "start_accost": db_company.start_accost,
                "end_accost": db_company.end_accost,
                "startrev": db_company.startrev,
                "endrev": db_company.endrev,
                "glrap": db_company.glrap,
                "startexp": db_company.startexp,
                "endexp": db_company.endexp,
                "acdate": db_company.acdate,
                "chkvat": db_company.chkvat,
            }
        ],
        "allRecords": db_company_count,
        "totalPage": total_pages,
        "currentPage": 1,
        "recordsPerPage": 10,
        "recordsInPage": 1,
        "status": "success"
    }

    return result_dict

@router.put("/{company_id}", response_model=dict)
async def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):    
    db_company = db.query(Company).filter(Company.company_id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    update_data = company.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company, key, value)     
    db.commit()
    db.refresh(db_company)  
    return {"message": "Company updated successfully", "company_id": db_company.company_id}

@router.delete("/{company_id}", response_model=dict)
async def delete_company(company_id: int, db: Session = Depends(get_db)):   
    db_company = db.query(Company).filter(Company.company_id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}