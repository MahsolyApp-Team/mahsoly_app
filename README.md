<div align="center">
  
  <h1>🌱 Mahsoly Backend API</h1>

  <p>
    <strong>AI-powered agricultural backend API built with FastAPI.</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-0.133.0-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License" />
  </p>

</div>

---

> **Mahsoly** provides functionalities for plant disease detection, crop recommendation, and fertilizer recommendation using external AI models. It also includes robust user authentication with OTP-based verification, password management, and email notifications.

---

## 📋 Prerequisites and Dependencies

Before you begin, ensure you have the following installed on your system:

### 💻 System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: At least 1GB (for running the local server)

### 🛠️ Required Software & Tools
- **Git** (to clone the repository)
- **Python 3.9+**
- **pip** (Python package manager)
- **venv** (Python virtual environment module)

### 📚 Frameworks & Libraries
- **FastAPI**, **SQLAlchemy**, **Alembic**, **Passlib**, **python-jose**

### 🌐 External Services
- **Cloudinary**: Cloudinary account and API credentials for image uploads.
- **Email/SMTP Server**: An active SMTP account (e.g., Gmail, SendGrid) to send OTP verification emails.
- **Hugging Face APIs**: Relies on Hugging Face spaces for AI inferences (requires an active internet connection).
- **Database**: SQLite (default, no setup required) or PostgreSQL.

---

## 🚀 Installation Steps

Follow these exact steps to get the project onto your local machine:

**1. Clone the repository**:
Open your terminal or command prompt and run:
```bash
git clone https://github.com/yourusername/mahsoly_app.git
cd mahsoly_app
```

**2. Configure the environment (Virtual Environment)**:
It's highly recommended to use a virtual environment to isolate project dependencies.
```bash
python -m venv venv
```

**Activate the virtual environment**:
- On **Windows**:
  ```powershell
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

**3. Install dependencies**:
With your virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup & Configuration

You must set up your environment variables before running the application or database migrations.

**1. Create the configuration file**:
Create a new file named `.env` in the root directory of the project (the same folder as `main.py`).

**2. Add Environment Variables**:
Copy the following structure into your `.env` file and replace the placeholder values with your actual credentials:

```env
# 🗄️ Database Configuration
# For local testing, you can use SQLite:
DATABASE_URL=sqlite:///./mahsoly_app.db
# For production, use PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/mahsoly_db

# 🔐 Security
SECRET_KEY=your_super_secret_jwt_key

# ☁️ Cloudinary Setup (For Image Uploads)
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# 📧 Email/SMTP Setup (For sending OTPs)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password
```

**3. Database Setup**:
Initialize your database schema by running the Alembic migrations. Ensure your `.env` is configured correctly before running this:
```bash
alembic upgrade head
```

---

## 🔨 Compilation Steps

This project is built with **Python**, which is an interpreted language. Therefore, **there are no explicit compilation steps required** to build this project. You simply run the source code directly! 🎉

---

## 🏃 Run Instructions

Once your dependencies are installed, environment variables are set, and the database is configured, you can start the application.

**1. Start the FastAPI server**:
Run the following command in your terminal from the root directory:
```bash
uvicorn main:app --reload
```

**2. Access the Application**:
- The API will be running locally at: `http://127.0.0.1:8000`
- You can interact with all endpoints visually via the automatic Swagger UI documentation at: **`http://127.0.0.1:8000/docs`**

**3. Stopping the Application**:
To stop the server, press `Ctrl + C` in your terminal.

---

<div align="center">
  <i>Built with ❤️ for better agriculture.</i>
</div>
