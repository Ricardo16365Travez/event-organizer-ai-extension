import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres_db:5432/event_db")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
