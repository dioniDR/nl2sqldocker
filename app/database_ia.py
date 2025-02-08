from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine_ia = create_engine(DATABASE_URL)
SessionLocalIA = sessionmaker(autocommit=False, autoflush=False, bind=engine_ia)
BaseIA = declarative_base()
