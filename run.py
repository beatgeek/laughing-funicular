#!/usr/bin/env python3
"""Entry point for the Content Journey Finder application."""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.app import app

if __name__ == '__main__':
    app.run()
