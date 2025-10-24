@echo off
REM Discord Clone - Local Development Setup Script (Windows)

echo.
echo ================================================
echo Discord Clone - Development Setup (Windows)
echo ================================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Python is not installed or not in PATH
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Node.js is not installed or not in PATH
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do echo [OK] %%i

REM Backend Setup
echo.
echo [INFO] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt -q

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file...
    copy .env.example .env
    echo [WARNING] Please configure .env with your database credentials
) else (
    echo [OK] .env file exists
)

cd ..

REM Frontend Setup
echo.
echo [INFO] Setting up Frontend...
cd frontend

REM Install Node dependencies
if not exist "node_modules" (
    echo [INFO] Installing Node dependencies...
    call npm install --quiet
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file...
    copy .env.example .env
    echo [OK] Frontend .env created
) else (
    echo [OK] .env file exists
)

cd ..

echo.
echo ================================================
echo [OK] Setup Complete!
echo ================================================

echo.
echo [INFO] Next steps:
echo 1. Configure backend\.env with your PostgreSQL connection
echo 2. Start PostgreSQL service (if not already running)
echo 3. In one terminal, run: cd backend ^& venv\Scripts\activate.bat ^& uvicorn main:app --reload
echo 4. In another terminal, run: cd frontend ^& npm run dev
echo 5. Open http://localhost:5173 in your browser

echo.
echo [INFO] Database Setup:
echo On Windows:
echo   - Install PostgreSQL from https://www.postgresql.org/download/windows/
echo   - Use pgAdmin to create database 'discord_clone'
echo   - Or use: psql -U postgres -c "CREATE DATABASE discord_clone;"

echo.
echo [INFO] Useful commands:
echo Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --reload
echo   [API docs will be available at: http://localhost:8000/docs]
echo.
echo Frontend:
echo   cd frontend
echo   npm run dev
echo   [Frontend will be available at: http://localhost:5173]

pause
