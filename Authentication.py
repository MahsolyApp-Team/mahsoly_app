from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User,CreateUser,LoginRequest,VerifyOTP
from security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
import random
from email_utils import send_otp_email


def generate_otp():
    return str(random.randint(100000, 999999))

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_input: CreateUser   , db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_input.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    otp = generate_otp()
    new_user = User(
        name =user_input.name,
        email=user_input.email,
        password=hash_password(user_input.password),
        otp_code=otp,
        otp_expiry=datetime.utcnow() + timedelta(minutes=5),
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    send_otp_email(user_input.email, otp)
    access_token = create_access_token({"sub": new_user.email})
    return {"message": "OTP sent to your email"}

@router.post("/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.otp_code == data.otp).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    user.is_verified = True
    user.otp_code = None
    user.otp_expiry = None
    db.commit()
    return {"message": "Account verified successfully"}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Verify your account first")
    
    access_token = create_access_token({"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }