import os
import sys
from pathlib import Path
from dotenv import load_dotenv 

load_dotenv() 
os.getenv("")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
