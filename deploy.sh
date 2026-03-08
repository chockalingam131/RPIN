#!/bin/bash

echo "========================================"
echo "RPIN - Vercel Deployment Helper"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed!"
    echo "Please install Git from: https://git-scm.com/downloads"
    echo ""
    exit 1
fi

echo "[OK] Git is installed"
echo ""

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "[OK] Git repository initialized"
    echo ""
fi

# Add all files
echo "Adding files to Git..."
git add .
echo "[OK] Files added"
echo ""

# Commit
echo "Committing files..."
git commit -m "Deploy RPIN application"
if [ $? -ne 0 ]; then
    echo "[INFO] No changes to commit or already committed"
fi
echo ""

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "========================================"
    echo "SETUP REQUIRED"
    echo "========================================"
    echo ""
    echo "Please follow these steps:"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Create a new repository named: rpin"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo "[ERROR] No URL provided"
        exit 1
    fi
    
    git remote add origin "$REPO_URL"
    echo "[OK] Remote added"
    echo ""
fi

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to push to GitHub"
    echo "Please check your GitHub credentials and try again"
    echo ""
    exit 1
fi

echo "[OK] Code pushed to GitHub"
echo ""

echo "========================================"
echo "SUCCESS!"
echo "========================================"
echo ""
echo "Your code is now on GitHub!"
echo ""
echo "Next steps:"
echo "1. Go to: https://vercel.com/new"
echo "2. Sign in with GitHub"
echo "3. Import your 'rpin' repository"
echo "4. Click Deploy"
echo "5. Wait 2-3 minutes"
echo "6. Your app will be live!"
echo ""
echo "========================================"
