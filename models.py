# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class FamilyDetails(Base):
    __tablename__ = "family_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable = False)
    aadhar_number = Column(String(15), nullable=True, unique=True)
    is_active = Column(Boolean, default=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())