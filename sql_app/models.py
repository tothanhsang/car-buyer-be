from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from config_db.db import Base

class CarModel(Base):
  __tablename__ = "car-model"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(80), nullable=False, unique=True, index=True)
  description = Column(String(200))
  car_brand_id = Column(Integer, ForeignKey('car-brand.id'), nullable=False)
  def __repr__(self):
      return 'CarModel(name=%s, description=%s, car_brand_id=%s)' % (self.name, self.description, self.car_brand_id)
      
class CarBrand(Base):
  __tablename__ = "car-brand"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(80), nullable=False, unique=True)
  img_url = Column(String(120))
  description = Column(String(200))
  status = Column(Boolean)
  last_update = Column(String(200))
  number_model = Column(Integer)
  car_models = relationship("CarModel", primaryjoin="CarBrand.id == CarModel.car_brand_id", cascade="all, delete-orphan")
  def __repr__(self):
      return 'CarBrand(name=%s, img_url=%s, description=%s)' % (self.name, self.img_url, self.description)
