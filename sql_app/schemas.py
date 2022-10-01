from typing import List, Optional
from pydantic import BaseModel

# Schemas Item
class ItemBase(BaseModel):
  name: str
  price: float
  description: Optional[str] = None

class ItemCreate(ItemBase):
  pass

class Item(ItemBase):
  id: int
  store_id: int

  class Config:
    orm_mode = True

# Schemas Store
class StoreBase(BaseModel):
  name: str

class StoreCreate(StoreBase):
  pass

class Store(StoreBase):
  id: int
  items: List[Item] = []

  class Config:
    orm_mode = True
