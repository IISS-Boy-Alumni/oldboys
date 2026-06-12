import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app

application = create_app("production")
