import datetime
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from config_db.db import engine, get_db
import uvicorn

import cloudinary
import cloudinary.uploader

from sql_app.crud import CarModelRepo, CarBrandRepo
import sql_app.models as models
import sql_app.schemas as schemas

app = FastAPI(title="Sample FastAPI Application",
description = "Sample FastAPI Application with Swagger and Sqlalchemy",
version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
  base_error_message = f"Failed to execute: {request.method}: {request.url}"
  return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

# Car Model
@app.post('/car-models', tags=["CarModel"], response_model=schemas.CarModel, status_code=201)
async def create_car_model(car_model_request: schemas.CarModelCreate, db: Session = Depends(get_db)):
  """
  Create an CarModel it in the database
  """
  db_car_model = CarModelRepo.fetch_by_name(db, name=car_model_request.name)
  if db_car_model:
    raise HTTPException(status_code=400, detail="Car Model already exists!")
  db_car_brand = CarBrandRepo.fetch_by_id(db, car_model_request.car_brand_id)
  if db_car_brand is None:
    raise HTTPException(status_code=400, detail="Store no exists, pls enter correct store ID!")
  return await CarModelRepo.create(db=db, car_model=car_model_request)

@app.get('/car-models', tags=["CarModel"], response_model=List[schemas.CarModel])
def get_all_car_models(name: Optional[str] = None, db: Session=Depends(get_db)):
  """
  Get all the Car Models stored in database
  """
  if name:
    car_models = []
    db_car_model = CarModelRepo.fetch_by_name(db, name)
    car_models.append(db_car_model)
    return car_models
  else:
    return CarModelRepo.fetch_all(db)

@app.get('/car-models/{car_model_id}', tags=["CarModel"], response_model=schemas.CarModel)
def get_car_model(car_model_id: int, db: Session = Depends(get_db)):
  """
   Get the Car Model with the given ID provided by User stored in database
  """
  db_car_model = CarModelRepo.fetch_by_id(db, car_model_id)
  if db_car_model is None:
    raise HTTPException(status_code=404, detail="Car Model not found with the given ID")
  return db_car_model

@app.delete('/car-models/{car_model_id}', tags=["CarModel"])
async def delete_car_model(car_model_id: int, db: Session=Depends(get_db)):
  """
  Delete the Car Model with the given ID provided by User stored in database
  """
  db_car_model = CarModelRepo.fetch_by_id(db, car_model_id)
  if db_car_model is None:
    raise HTTPException(status_code=404, detail="Item not found with the given ID")
  await CarModelRepo.delete(db, car_model_id)
  return "Car Model deleted successfully"

@app.put('/car-models/{car_model_id}', tags=["CarModel"], response_model=schemas.CarModel)
async def update_car_model(car_model_id: int, car_model_request: schemas.CarModel, db: Session=Depends(get_db)):
  """
  Update an Car Model stored in the database
  """
  db_car_model = CarModelRepo.fetch_by_id(db, car_model_id)
  if db_car_model:
    update_car_model_encoded = jsonable_encoder(car_model_request)
    db_car_model.name = update_car_model_encoded['name']
    db_car_model.description = update_car_model_encoded['description']
    db_car_model.car_brand_id = update_car_model_encoded['car_brand_id']
    return await CarModelRepo.update(db=db, car_model_data=db_car_model)
  else:
    raise HTTPException(status_code=404, detail="Car Model not found with the given ID")

# Store
@app.post('/car-brands', tags=["CarBrand"], status_code=201)
async def create_car_brand(
  name: str = Form(),
  description: Optional[str] = Form(),
  status: bool = Form(),
  last_update: str = Form(),
  number_model: int = Form(),
  img_file: Optional[UploadFile] = File(None),
  db: Session = Depends(get_db)
):
  """
  Create an Car Brand it in the database
  """
  db_car_brand = CarBrandRepo.fetch_by_name(db, name=name)
  if db_car_brand:
    raise HTTPException(status_code=400, detail="Car Brand already exists!")
  result = cloudinary.uploader.upload(img_file.file)
  return await CarBrandRepo.create(db=db, name=name, img_url=result.get("url"), description=description, status=status, last_update=last_update, number_model=number_model)

@app.get('/car-brands', tags=["CarBrand"])
async def get_all_car_brands(name: Optional[str]=None, db: Session=Depends(get_db)):
  """
  Get all the Car Brands stored in database
  """
  if name:
    car_brands = []
    db_car_brand = CarBrandRepo.fetch_by_name(db, name)
    if db_car_brand is None:
      return []
    else:
      car_brands.append(db_car_brand)
      return car_brands
  else:
    return CarBrandRepo.fetch_all(db)

@app.get('/car-brands/{car_brand_id}', tags=["CarBrand"])
def get_car_brand(car_brand_id: int, db: Session = Depends(get_db)):
  """
   Get the Car Brand with the given ID provided by User stored in database
  """
  db_car_brand = CarBrandRepo.fetch_by_id(db, car_brand_id)
  if db_car_brand is None:
    raise HTTPException(status_code=404, detail="Car Model not found with the given ID")
  return db_car_brand

@app.delete('/car-brands/{car_brand_id}', tags=["CarBrand"])
async def delete_car_model(car_brand_id: int, db: Session=Depends(get_db)):
  """
  Delete the Car Brand with the given ID provided by User stored in database
  """
  db_car_brand = CarBrandRepo.fetch_by_id(db, car_brand_id)
  if db_car_brand is None:
    raise HTTPException(status_code=404, detail="Item not found with the given ID")
  await CarBrandRepo.delete(db, car_brand_id)
  return "Car Model deleted successfully"

@app.put('/car-brands/{car_brand_id}', tags=["CarBrand"])
async def update_car_model(
  car_brand_id: int, 
  name: str = Form(),
  description: Optional[str] = Form(),
  status: bool = Form(),
  last_update: str = Form(),
  number_model: int = Form(),
  img_file: Optional[UploadFile] = File(None),
  db: Session=Depends(get_db)
):
  """
  Update an Car Brand stored in the database
  """
  db_car_brand = CarBrandRepo.fetch_by_id(db, car_brand_id)
  if db_car_brand:
    db_car_brand.name = name
    db_car_brand.description = description
    db_car_brand.status = status
    db_car_brand.last_update = last_update
    db_car_brand.number_model = number_model
    if img_file:
      result = cloudinary.uploader.upload(img_file.file)
      db_car_brand.img_url = result.get("url")
    return await CarBrandRepo.update(db=db, car_band_data=db_car_brand)
  else:
    raise HTTPException(status_code=404, detail="Car Model not found with the given ID")

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
