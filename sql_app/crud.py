from sqlalchemy.orm import Session
from . import models, schemas

class CarModelRepo:
  async def create(db:Session, car_model: schemas.CarModelCreate):
    db_car_model = models.CarModel(name=car_model.name, description=car_model.description, car_brand_id=car_model.car_brand_id)
    db.add(db_car_model)
    db.commit()
    db.refresh(db_car_model)
    return db_car_model

  def fetch_by_id(db: Session, _id):
    return db.query(models.CarModel).filter(models.CarModel.id == _id).first()

  def fetch_by_name(db: Session, name):
    return db.query(models.CarModel).filter(models.CarModel.name == name).first()

  def fetch_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CarModel).offset(skip).limit(limit).all()

  async def delete(db: Session, car_model_id):
    db_car_model = db.query(models.CarModel).filter_by(id=car_model_id).first()
    db.delete(db_car_model)
    db.commit()

  async def update(db: Session, car_model_data):
    update_car_model = db.merge(car_model_data)
    db.commit()
    return update_car_model

class CarBrandRepo:
  async def create(db: Session, name: str, img_url: str, description: str, status: str, last_update: str, number_model: str):
    db_car_brand = models.CarBrand(name=name, img_url=img_url, description=description, status=status, last_update=last_update, number_model=number_model)
    db.add(db_car_brand)
    db.commit()
    db.refresh(db_car_brand)
    return db_car_brand
  
  def fetch_by_id(db: Session, _id: int):
    return db.query(models.CarBrand).filter(models.CarBrand.id == _id).first()
  
  def fetch_by_name(db: Session, name: str):
    return db.query(models.CarBrand).filter(models.CarBrand.name == name).first()

  def fetch_all(db: Session, skip: int=0, limit: int=100):
    return db.query(models.CarBrand).offset(skip).limit(limit).all()
  
  async def delete(db: Session, _id: int):
    db_car_brand = db.query(models.CarBrand).filter_by(id=_id).first()
    db.delete(db_car_brand)
    db.commit()

  async def update(db: Session, car_band_data):
    update_car_brand = db.merge(car_band_data)
    db.commit()
    return update_car_brand
