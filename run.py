#!/usr/bin/env python3
"""Entry point for the Content Journey Finder application."""
import sys
import os
import uvicorn

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("app.app:app", host='0.0.0.0', port=port, reload=True)
