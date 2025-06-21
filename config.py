import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TEST_TOKEN") 
# or os.getenv("TOKEN")
