from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx,cloudinary_config
from datetime import datetime
from database import get_db
from models import Scan, Scanimage
from verify import get_current_user
from upload import upload_image_to_cloudinary   
import traceback

router = APIRouter()

HF_API_URL = "https://mahmoudiraqi21-plant-disease-classifier.hf.space/predict" 

@router.post("/scan")
async def scan_plant(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        contents = await file.read()
        image_url = upload_image_to_cloudinary(contents)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                HF_API_URL,
                files={"file": (file.filename, contents, file.content_type)},timeout=50.0
            )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="API Model failed")
        data = response.json()
        label = data.get("prediction")
        confidence = data.get("confidence")
        plant_name = None
        disease_name = None
        if label:   
            parts = label.split("___")
            if len(parts) == 2:
                plant_name = parts[0]
                disease_name = parts[1]
        new_scan = Scan(
            user_id=user.id,
            plant_name=plant_name,
            disease_name=disease_name,
            confidence=confidence,
            created_at=datetime.now()
        )
        db.add(new_scan)
        db.commit()
        db.refresh(new_scan)
        image = Scanimage(
            scan_id=new_scan.id,
            image_url=image_url
        )
        db.add(image)
        db.commit()
        return {
            "scan_id": new_scan.id,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "confidence": confidence,
            "image_url": image_url
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error") 