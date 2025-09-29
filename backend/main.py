"""
Main entry point for the BemaSnap Backend API.
Run with: python main.py
"""

import sys
import os
import uvicorn

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[os.getcwd()]
    )