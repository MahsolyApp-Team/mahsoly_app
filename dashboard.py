from dotenv import load_dotenv
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from verify import get_current_user
from database import get_db

load_dotenv()

POWER_BI_URL = os.getenv("POWER_BI_URL")
API_KEY = os.getenv("API_KEY")

router = APIRouter()
@router.get("/Dashboard")
def get_report(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
    ):
    
    return {
        "url": POWER_BI_URL
    }