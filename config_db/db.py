from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_db.config import settings
import cloudinary

# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

cloudinary.config( 
  cloud_name = "dzs3cc3sc", 
  api_key = "555513995258914", 
  api_secret = "tBf0O15ZIcRTks8aCaWSZJ536Ws" 
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
