# Vercel entrypoint for FastAPI
# This file imports the app from the root-level api.py

import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import from api.py
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import the FastAPI app instance
from api import app

# Vercel will look for an 'app' variable in this module
__all__ = ["app"]
