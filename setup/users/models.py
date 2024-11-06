from sqlalchemy import Column, Integer, String, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'member'

    m_id = Column(Integer, primary_key=True, autoincrement=True)
    m_code = Column(String(10))
    m_firstname = Column(String(100))
    m_lastname = Column(String(100)) 
    m_middlename = Column(String(100))
    m_name = Column(String(100))
    m_user = Column(String(100))
    m_pass = Column(String(100))
    m_status = Column(String(50))
    m_position = Column(String(100))
    m_type = Column(String(100), server_default='employee')
    m_login = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    m_email = Column(String(100))
    m_project = Column(String(45))
    m_department = Column(String(45))
    m_tel = Column(String(20))
    uimg = Column(Text)
    compcode = Column(String(45))
    sign = Column(String(100))
    m_vender = Column(String(255))
    LoginStatus = Column(Integer)
    LastUpdate = Column(DateTime(timezone=True))
    user_type = Column(String(10), nullable=False, server_default='user')
    date_pass = Column(DateTime, server_default=text("'1970-01-01 01:00:00'"))
    dashboard = Column(String(100))
    lineid = Column(String(50))
    prekey = Column(String(100))
    user_status = Column(String(20))
    gender = Column(String(20))
# End of Selection



