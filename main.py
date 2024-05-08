import datetime
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from botiga_db import botiga_db


db_handler = botiga_db()

app = FastAPI()

class producte(BaseModel):
    name:str
    description: str
    company:str
    price:float
    units:int
    subcategory_id:int
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

@app.get("/product/")
def read_products():
    return db_handler.read_productes()

@app.get("/product/{id}")
def read_product():
    return db_handler.read_producte()


p = {"name": "elpro", "description": "ducto", "company": "micompa", "price": 123.45, "units": 1, "subcategory_id": 1}
print(db_handler.create_producte(p))
