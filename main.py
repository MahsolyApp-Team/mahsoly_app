from fastapi import FastAPI, Depends
from database import Base, engine
from Authentication import router as auth_router
from dashboard import router as dash_router
from AI_models import router as AI_router
from chatbot import router as chat_router
from verify import get_current_user
from models import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(AI_router)
app.include_router(chat_router)
app.include_router(dash_router)



@app.get("/home")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }