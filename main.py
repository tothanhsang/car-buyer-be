from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from db import engine, get_db
import uvicorn

import cloudinary
import cloudinary.uploader

from sql_app import models
from sql_app.crud import ItemRepo, StoreRepo
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

# Item
@app.post('/items', tags=["Item"], response_model=schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
  """
  Create an Item and Store it in the database
  """
  db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
  if db_item:
    raise HTTPException(status_code=400, detail="Item already exists!")
  db_store = StoreRepo.fetch_by_id(db, item_request.store_id)
  if db_store is None:
    raise HTTPException(status_code=400, detail="Store no exists, pls enter correct store ID!")
  return await ItemRepo.create(db=db, item=item_request)

@app.get('/items', tags=["Item"], response_model=List[schemas.Item])
def get_all_items(name: Optional[str] = None, db: Session=Depends(get_db)):
  """
  Get all the Items stored in database
  """
  if name:
    items = []
    db_item = ItemRepo.fetch_by_name(db, name)
    items.append(db_item)
    return items
  else:
    return ItemRepo.fetch_all(db)

@app.get('/items/{item_id}', tags=["Item,"], response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
  """
   Get the Item with the given ID provided by User stored in database
  """
  db_item = ItemRepo.fetch_by_id(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found with the given ID")
  return db_item

@app.delete('/items/{item_id}', tags=["Item"])
async def delete_item(item_id: int, db: Session=Depends(get_db)):
  """
  Delete the Item with the given ID provided by User stored in database
  """
  db_item = ItemRepo.fetch_by_id(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found with the given ID")
  await ItemRepo.delete(db, item_id)
  return "Item deleted successfully"

@app.put('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
async def update_item(item_id: int, item_request: schemas.Item, db: Session=Depends(get_db)):
  """
  Update an Item stored in the database
  """
  db_item = ItemRepo.fetch_by_id(db, item_id)
  if db_item:
    update_item_encoded = jsonable_encoder(item_request)
    db_item.name = update_item_encoded['name']
    db_item.price = update_item_encoded['price']
    db_item.description = update_item_encoded['description']
    db_item.store_id = update_item_encoded['store_id']
    return await ItemRepo.update(db=db, item_data=db_item)
  else:
    raise HTTPException(status_code=404, detail="Item not found with the given ID")

# Store
@app.post('/stores', tags=["Store"], response_model=schemas.Store, status_code=201)
async def create_store(store_request: schemas.StoreBase, db: Session = Depends(get_db)):
  """
  Create an Store and Store it in the database
  """
  db_store = StoreRepo.fetch_by_name(db, name=store_request.name)
  if db_store:
    raise HTTPException(status_code=400, detail="Store already exists!")
  return await StoreRepo.create(db=db, store=store_request)

@app.get('/stores', tags=["Store"], response_model=List[schemas.Store])
def get_all_stores(name: Optional[str]=None, db: Session=Depends(get_db)):
  """
  Get all the Stores stored in database
  """
  if name:
    stores = []
    db_store = StoreRepo.fetch_by_name(db, name)
    stores.append(db_store)
    return stores
  else:
    return StoreRepo.fetch_all(db)

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_post(file: UploadFile = File(...), db: Session = Depends(get_db)):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    print("url: ", url)

if __name__ == "__main__":
    # uvicorn.run("main:app", port=9000, reload=True)
     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
