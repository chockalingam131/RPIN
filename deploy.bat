@echo off
echo ========================================
echo RPIN - Vercel Deployment Helper
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Check if this is a git repository
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo [OK] Git repository initialized
    echo.
)

REM Add all files
echo Adding files to Git...
git add .
echo [OK] Files added
echo.

REM Commit
echo Committing files...
git commit -m "Deploy RPIN application"
if errorlevel 1 (
    echo [INFO] No changes to commit or already committed
)
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo SETUP REQUIRED
    echo ========================================
    echo.
    echo Please follow these steps:
    echo.
    echo 1. Go to: https://github.com/new
    echo 2. Create a new repository named: rpin
    echo 3. Copy the repository URL
    echo.
    set /p REPO_URL="Enter your GitHub repository URL: "
    
    if "%REPO_URL%"=="" (
        echo [ERROR] No URL provided
        pause
        exit /b 1
    )
    
    git remote add origin %REPO_URL%
    echo [OK] Remote added
    echo.
)

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo [ERROR] Failed to push to GitHub
    echo Please check your GitHub credentials and try again
    echo.
    pause
    exit /b 1
)

echo [OK] Code pushed to GitHub
echo.

echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo Next steps:
echo 1. Go to: https://vercel.com/new
echo 2. Sign in with GitHub
echo 3. Import your 'rpin' repository
echo 4. Click Deploy
echo 5. Wait 2-3 minutes
echo 6. Your app will be live!
echo.
echo ========================================
pause
