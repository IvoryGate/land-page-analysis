import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    USR = os.getenv("USR")
    PASSWORD = os.getenv("PASSWORD")
    DATABASE = os.getenv("DATABASE")
    CHARSET = os.getenv("CHARSET")