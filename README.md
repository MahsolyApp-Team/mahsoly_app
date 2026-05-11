Mahsoly Backend API
Smart Agriculture Backend System powered by AI.
Built with FastAPI to provide crop recommendation, plant disease detection, authentication, image handling, and intelligent agricultural services.

Overview
Mahsoly Backend acts as the core server for the Mahsoly platform.
It handles:
User authentication
AI model communication
Plant disease detection
Crop recommendation
fertilizer recommendation
Image uploads
Database management
Scan history storage
The backend communicates asynchronously with deployed AI models hosted on external servers such as Hugging Face Spaces.

Features:
JWT Authentication
Plant Disease Detection
Crop Recommendation System
fertilizer recommendation System
Cloudinary Image Upload
SQLAlchemy ORM
Async API Requests using HTTPX
Swagger API Documentation
Scan History Management

Tech Stack
Python --> Main Programming Language
FastAPI --> Backend Framework
SQLAlchemy	--> ORM
PostgreSQL -->	Database
JWT	--> Authentication
Pydantic -->	Validation
HTTPX	--> Async HTTP Requests
Cloudinary --> Image Hosting
Uvicorn -->	ASGI Server

Before running this project, make sure you have the following installed.
1-Programming Languages: Python3.10+
2-Frameworks & Libraries:
fastapi
uvicorn
sqlalchemy
pydantic
python-jose
passlib
bcrypt
httpx
cloudinary
python-dotenv
python-multipart

Install all dependencies using: pip install -r requirements.txt

Required Software & Tools:
Git	--> Version Control
Python	--> Runtime Environment
pip	--> Package Manager
PostgreSQL -->	Production Database

System Requirements: 
OS	--> Windows / Linux / macOS
RAM	--> 4 GB
Storage	--> 1 GB Free Space
Internet	--> Required for AI APIs

External Services : 
Vercel --> APP Hosting
Hugging Face --> Spaces	AI Model Hosting
Cloudinary	--> Image Storage

Installation Steps:
1-Clone the Repository:
git clone https://github.com/your-username/mahsoly-backend.git
2-Create Virtual Environment (Windows):
python -m venv venv
3-Install Dependencies:
pip install -r requirements.txt

Environment Setup & Configuration:
1-Create a .env file in the root directory.
Environment Variables:
SECRET_KEY	--> JWT Secret Key
DATABASE_URL	--> Database Connection URL
CLOUD_NAME	--> Cloudinary Cloud Name
CLOUDINARY_API_KEY	--> Cloudinary API Key
CLOUDINARY_API_SECRET	--> Cloudinary Secret
CROP_API	--> Crop Recommendation Model API
DISEASE_API	--> Disease Detection Model API
fertilizer_API --> fertilizer Recommendation Model API
2-Run Instructions:
uvicorn main:app --reload

AI Model Integration:
The backend communicates with external AI models hosted on Hugging Face Spaces using asynchronous HTTP requests.
Workflow:
Client Request
      ↓
FastAPI Backend
      ↓
AI Model API
      ↓
Prediction Response
      ↓
Database Storage
      ↓
Return Final Result

Main API Endpoints:   
Method	                    Endpoint	                  Description
POST	                      /register                  	Register new user
POST                        /verify_otp                 verifying otp 
POST                        /change_email               Update user's email
POST                        /confirm_email              verifying otp for new email
PUT                         /change_password            Update user's Password 
POST	                      /login	                    Login user
POST	                      /predict-crop	              Crop recommendation
POST	                      /scan           	          Disease detection
POST                        /fertilizer_recommendation  fertilizer recommendation

Authentication:
The project uses JWT Bearer Authentication.
Example Authorization Header: Authorization: Bearer YOUR_ACCESS_TOKEN

Image Upload Workflow
User Uploads Image
        ↓
FastAPI Receives Image
        ↓
Upload to Cloudinary
        ↓
Send Image to AI Model
        ↓
Store Result in Database
        ↓
Return Prediction Response

Author:
Ismail Abdalaziz Ibrahim
Backend Developer | FastAPI Developer | AI Enthusiast



















