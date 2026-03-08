"""
Vercel serverless function entry point for RPIN API
Standalone version that works without complex imports
"""
from app import app

# Export the app for Vercel
handler = app

