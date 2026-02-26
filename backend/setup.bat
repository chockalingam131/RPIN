@echo off
REM RPIN Backend Setup Script for Windows

echo 🚀 Setting up RPIN Backend...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist models mkdir models
if not exist data mkdir data

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: python main.py
echo 3. Visit: http://localhost:8000/docs
pause
