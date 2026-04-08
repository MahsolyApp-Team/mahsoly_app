from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    scans = relationship("Scan", back_populates="user", cascade="all, delete")
    
class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plant_name = Column(String, nullable=True)
    disease_name = Column(String)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="scans")
    images = relationship("Scanimage", back_populates="scan", cascade="all, delete")

class Scanimage(Base):
    __tablename__ = "scan_images"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    scan = relationship("Scan", back_populates="images")
    
class CreateUser(BaseModel):
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str