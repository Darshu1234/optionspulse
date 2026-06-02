from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os

Base = declarative_base()




load_dotenv()
password = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/greekdesk"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

