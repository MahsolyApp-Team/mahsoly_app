from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx,cloudinary_config
from datetime import datetime
from database import get_db
from models import Scan, Scanimage,Cropmodel,fertilizer
from verify import get_current_user
from upload import upload_image_to_cloudinary   
import traceback
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

router = APIRouter()

REC_API = os.getenv("recommendation_model")
Crop_API = os.getenv("crop_model")
fertilizer_API = ("fertilizer_model")

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
                files={
                    "file": (
                        file.filename,
                        contents,
                        file.content_type
                    )
                },
                timeout=100.0
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="AI Model API failed"
            )
        result = response.json()
        
        if "prediction" not in result:
            return {
                "message": result.get("message"),
                "tips": result.get("tips", [])
            }
        
        label = result.get("prediction")
        confidence = result.get("confidence")
        plant_name = None
        disease_name = None
        
        if label:
            parts = label.split(" ", 1)
            if len(parts) == 2:
                plant_name = parts[0]
                disease_name = parts[1]
        
        treatment_plan = result.get("treatment_plan", {})
        symptoms = None
        treatment = None
        prevention = None
        if isinstance(treatment_plan, dict):
            symptoms = treatment_plan.get("symptoms")
            treatment = treatment_plan.get("treatment")
            prevention = treatment_plan.get("prevention")
        elif isinstance(treatment_plan, str):
            treatment = treatment_plan
        
        new_scan = Scan(
            user_id=user.id,
            plant_name=plant_name,
            disease_name=disease_name,
            confidence=confidence,
            created_at=datetime.now(),
        )
        db.add(new_scan)
        db.flush()
        
        image = Scanimage(
            scan_id=new_scan.id,
            image_url=image_url
        )
        db.add(image)
        db.commit()
        db.refresh(new_scan)
        
        return {
            "scan_id": new_scan.id,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "confidence": confidence,
            "image_url": image_url,
            "symptoms": symptoms,
            "treatment": treatment,
            "prevention": prevention
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
        explanation = result.get("explanation")
        return {
            "recommended_crop": crop,
            "explanation ": explanation
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error")

@router.post("/fertilizer-recommendation")
async def fertilizer_recommendation(
    data: fertilizer,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                fertilizer_API,
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
        predicted_fertilizer = result.get("predicted_fertilizer")
        confidence = result.get("confidence")
        explanation = result.get("explanation")
        return {
            "predicted_fertilizer": predicted_fertilizer,
            "confidence ": confidence,
            "explanation": explanation
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error")