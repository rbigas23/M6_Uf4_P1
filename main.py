import datetime
from typing import List, Union
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
def read_product(id:int):
    return db_handler.read_producte(id)

@app.post("/create/")
def create_producte(producte: producte):
    try:
        db_handler.create_producte(producte.dict())
        return {"status": "Producte afegit correctament"}
    except Exception as e:
        return {"status": -1, "message": f"Error afegint el producte: {e}"}
    
@app.post("/creates/")
def create_productes(productes: List[producte]):
    results = []
    for producte in productes:
        try:
            db_handler.create_producte(producte.dict())
            results.append({"status": "Producte afegit correctament"})
        except Exception as e:
            results.append({"status": -1, "message": f"Error afegint el producte: {e}"})
    return results

@app.delete("/product/{id}")
def delete_producte(id: int):
    success = db_handler.delete_producte(id)
    return {"status": "Producte eliminat correctament"} if success else {"status": "Producte no trobat"}

@app.put("/product/{id}")
def update_producte(id: int, name: str):
    try:
        if db_handler.update_producte(id, name):
            return {"status": "S'ha modificat correctament"}
        else:
            return {"status": -1, "message": "Error modificant el producte"}
    except Exception as e:
        return {"status": -1, "message": f"Error modificant el producte: {e}"}
    
@app.get("/productAll")
def read_productes_with_details():
    try:
        products = db_handler.read_productes_details()
        return products
    except Exception as e:
        return {"status": -1, "message": f"Error obteniendo los productos: {e}"}



#p = {"name": "elpro", "description": "ducto", "company": "micompa", "price": 123.45, "units": 1, "subcategory_id": 1}
#print(db_handler.create_producte(p))
