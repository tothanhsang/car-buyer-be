from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import cloudinary

# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

cloudinary.config( 
  cloud_name = "dgk4wg0qm", 
  api_key = "866856679158744", 
  api_secret = "RpNTOTi9sJmv8XrSjIAwgVdvCIs" 
)

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
