from typing import List, Optional
from pydantic import BaseModel

# Schemas Car Model
class CarModelBase(BaseModel):
  name: str
  description: Optional[str] = None
  car_brand_id: int

class CarModelCreate(CarModelBase):
  pass

class CarModel(CarModelBase):
  id: int

  class Config:
    orm_mode = True

# Schemas Car Brand
class CarBrandBase(BaseModel):
  name: str
  img_url: str
  description: Optional[str] = None
  status: bool
  last_update: str
  number_model: int

class CarBrandCreate(CarBrandBase):
  pass

class CarBrand(CarBrandBase):
  id: int
  car_models: List[CarModel] = []

  class Config:
    orm_mode = True
