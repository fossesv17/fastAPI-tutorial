from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    brand: Optional[str] = None
    price: float

class UpdateItem(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None


app = FastAPI()

items = {}

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/items/{item_id}')
def get_item(item_id : int = Path(None, description='The ID of the item', gt=0), name : Optional[str] = None):
    return items[item_id]

@app.post('/add-item/{item_id}')
def add_item(item_id : int, item: Item):
    if item_id in items:
        return {'Error' : 'Item already exist'}

    items[item_id] = item
    return items[item_id]

@app.put('/update-item/{item_id}')
def update_item(item_id : int, item: UpdateItem):
    if item_id not in items:
        return {'Error' : 'The item does not exist'}

    if item.name:
        items[item_id].name = item.name

    if item.brand:
        items[item_id].brand = item.brand

    if item.price:
        items[item_id].price = item.price

    return items[item_id]

@app.delete('/delete-item')
def delete_item(item_id : int = Query(..., description='ID of item to delete', gt=0)):
    if item_id not in items:
        return {'Error' : 'The item does not exist'}

    del items[item_id]
    return {'Success' : 'Item deleted'}