import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    load_dotenv()    
except:
    print("Can not read .env file")

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/library')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()