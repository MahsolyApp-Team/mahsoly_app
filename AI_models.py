from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx,cloudinary_config
from datetime import datetime
from database import get_db
from models import Scan, Scanimage,Cropmodel
from verify import get_current_user
from upload import upload_image_to_cloudinary   
import traceback

router = APIRouter()

REC_API =  "https://mahmoudiraqi21-plant-disease-detection.hf.space/predict" 
Crop_API = "https://mahmoudiraqi21-crop-recommendation.hf.space/predict"

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
                REC_API,
                files={"file": (file.filename, contents, file.content_type)},timeout=100.0
            )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="API Model failed")
        data = response.json()
        if "prediction" not in data:
            return {
                "message": data.get("message"),
                "tips": data.get("tips", [])
    }
        label = data.get("prediction")
        confidence = data.get("confidence")
        plant_name = None
        disease_name = None
        if label:
            parts = label.split(" ", 1)  
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

@router.post("/predict-crop")
async def predict_crop(
    data: Cropmodel,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                Crop_API,
                json=data.model_dump(),
                timeout=100.0
            )

        if response.status_code != 200:
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "API Model failed",
                    "status_code": response.status_code,
                    "response": response.text
                }
            )

        result = response.json()

        if "recommended_crop" not in result:
            return {
                "message": result.get("message"),
                "tips": result.get("tips", [])
            }

        crop = result.get("recommended_crop")

        return {
            "recommended_crop": crop
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error")