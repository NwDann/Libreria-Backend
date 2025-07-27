from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import dotenv_values

config = dotenv_values(".env")
DATABASE_URL = config.get("DATABASE_URL")

print(f"Database URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

DbSession = Annotated[Session, Depends(get_db)]