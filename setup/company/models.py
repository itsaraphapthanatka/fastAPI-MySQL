from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"

    company_id = Column(Integer, primary_key=True, index=True)
    company_code = Column(String(20), nullable=True)
    company_taxnum = Column(String(50), nullable=True)
    company_name = Column(String(100), nullable=True)
    company_address = Column(String(255), nullable=True)
    company_tel = Column(String(100), nullable=True)
    company_fax = Column(String(100), nullable=True)
    company_email = Column(String(100), nullable=True)
    company_contact = Column(String(100), nullable=True)
    comp_img = Column(String, nullable=True)
    compcode = Column(String(45), nullable=True)
    ic_type = Column(String(10), nullable=True, default='fifo')
    start_accost = Column(String(100), nullable=True)
    end_accost = Column(String(100), nullable=True)
    startrev = Column(String(100), nullable=True)
    endrev = Column(String(100), nullable=True)
    glrap = Column(String(100), nullable=True)
    startexp = Column(String(100), nullable=True)
    endexp = Column(String(100), nullable=True)
    acdate = Column(String, nullable=True)  # Changed from DATE to String for SQLAlchemy
    chkvat = Column(String(100), nullable=True)
    glrar = Column(String(100), nullable=True)
    dptandproj = Column(String(100), nullable=True)
    useradd = Column(String(100), nullable=True)
    createdate = Column(String, nullable=True)  # Changed from DATETIME to String
    useredit = Column(String(100), nullable=True)
    editdate = Column(String, nullable=True)  # Changed from DATETIME to String
    userdel = Column(String(100), nullable=True)
    deldate = Column(String, nullable=True)  # Changed from DATETIME to String
    updatetime = Column(String, nullable=True)  # Changed from DATETIME to String
    company_nameth = Column(String(255), nullable=True)
    company_add_en = Column(String(255), nullable=True)
    company_address2 = Column(String(255), nullable=True)
    company_address3 = Column(String(255), nullable=True)
    company_add_en2 = Column(String(255), nullable=True)
    company_add_en3 = Column(String(255), nullable=True)
    company_telen = Column(String(100), nullable=True)
    company_faxen = Column(String(100), nullable=True)
    company_emailen = Column(String(100), nullable=True)
    company_contacten = Column(String(200), nullable=True)
    compcodeen = Column(String(100), nullable=True)
    company_taxnumen = Column(String(100), nullable=True)
    site_url = Column(String(200), nullable=True)
    auto_post_gl = Column(String(2), nullable=True)
    wt_tax = Column(String(5), nullable=True)
    wt_taxen = Column(Integer, nullable=True)
