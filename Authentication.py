from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlalchemy.orm import Session
from database import get_db
from models import User,CreateUser,LoginRequest,VerifyOTP,ChangePassword,ChangeEmailRequest,change_email_otp,ForgotPassword,VerifyResetOtp,ResetPassword
from security import hash_password, verify_password, create_access_token,create_refresh_token
from datetime import datetime, timedelta
import random
from email_utils import send_otp_email
from verify import get_current_user
from jose import jwt,JWTError
from dotenv import load_dotenv
import os



def generate_otp():
    return str(random.randint(100000, 999999))

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_input: CreateUser   , db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_input.email).first()
    if db_user:
        if db_user.is_verified:
            raise HTTPException(status_code=400, detail="Email already exists")
        otp = generate_otp()
        db_user.otp_code = otp
        db_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.commit()
        send_otp_email(db_user.email, otp)
        return {"message": "OTP resent to your email"}
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

@router.post("/change-email")
def change_email(
    data: ChangeEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(User).filter(User.email == data.new_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    otp = generate_otp()
    current_user.otp_code = otp
    current_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
    current_user.new_email = data.new_email
    db.commit()
    send_otp_email(data.new_email, otp)
    return {"message": "OTP sent to new email"}

@router.post("/confirm-email-otp")
def confirm_email(
    data: change_email_otp,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if datetime.utcnow() > current_user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")
    current_user.email = current_user.new_email
    current_user.new_email = None
    current_user.otp_code = None
    db.commit()
    return {"message": "Email updated successfully"}

@router.put("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    if verify_password(data.new_password, current_user.password):
        raise HTTPException(status_code=400, detail="New password can not be the same")
    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="passwords does not match")
    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPassword,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = str(random.randint(100000, 999999))
    
    user.reset_otp = otp
    user.reset_otp_expiry = datetime.utcnow() + timedelta(minutes=5)
    db.commit()
    send_otp_email(data.email,otp)
    print("OTP:", otp)
    return {
        "message": "OTP sent",
        "email": user.email
    }
    
@router.post("/verify-reset-otp")
def verify_reset_otp(
    data: VerifyResetOtp,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.reset_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if datetime.utcnow() > user.reset_otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")
    return {
        "message": "OTP verified",
        "email": user.email
    }

@router.post("/reset-password")
def reset_password(
    data: ResetPassword,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    user.password = hash_password(data.new_password)
    user.reset_otp = None
    user.reset_otp_expiry = None
    db.commit()
    return {
        "message": "Password reset successful"
    }
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong email or password "
        )
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Verify your account first")
    
    access_token = create_access_token({"sub": user.email,"name":user.name})
    REFRESH_TOKEN = create_refresh_token({"sub": user.email,"name":user.name})
    
    return {
        "access_token": access_token,
        "REFRESH_TOKEN": REFRESH_TOKEN,
        "token_type": "bearer"
    }

ALGORITHM = "HS256"
@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        email = payload.get("sub")
        name=payload.get("name")
        new_access_token = create_access_token({"sub": email,"name":name})
        return {"access_token": new_access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")