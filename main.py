import datetime
from typing import List
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

# En este endpoint se llama a todos los productos con "/product"
@app.get("/product/")
def read_products():
    return db_handler.read_productes()

# En este endpoint se llama a un producto segun el ID "/product/{id}"
@app.get("/product/{id}")
def read_product(id:int):
    return db_handler.read_producte(id)

# En este endpoint se crea un producto "/create"
@app.post("/create/")
def create_producte(producte: producte):
    try:
        db_handler.create_producte(producte.dict())
        return {"status": "Producte afegit correctament"}
    except Exception as e:
        return {"status": -1, "message": f"Error afegint el producte: {e}"}
    
# En este endpoint se pueden crear mas de un producto "/creates"    
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

# En este endpoint se elimina un producto segun el ID "/product/{id}"
@app.delete("/product/{id}")
def delete_producte(id: int):
    success = db_handler.delete_producte(id)
    return {"status": "Producte eliminat correctament"} if success else {"status": "Producte no trobat"}


# En este endpoint se modifica el nombre de un producto segun el ID "/producto/{id}"
@app.put("/product/{id}")
def update_producte(id: int, name: str):
    try:
        if db_handler.update_producte(id, name):
            return {"status": "S'ha modificat correctament"}
        else:
            return {"status": -1, "message": "Error modificant el producte"}
    except Exception as e:
        return {"status": -1, "message": f"Error modificant el producte: {e}"}
    
# En este endpoint se llaman a todos los productos con unos detalles especificos: nombre de la categoria, nombre de la subcategoria, nombre del producto, marca del producto y el precio "/productAll"
@app.get("/productAll")
def read_productes_with_details():
    try:
        products = db_handler.read_productes_details()
        return products
    except Exception as e:
        return {"status": -1, "message": f"Error obteniendo los productos: {e}"}

# Aquest endpoint permet inserir tots els productes d'un fitxer csv a la base de dades
@app.get("/loadProducts/{filename}")
def load_products(filename:str):
    try:
        db_handler.load_products(filename)
        return {"status": "Productes carregats correctament"}
    except Exception as e:
        return {"status": -1, "message": f"Error afegint el producte: {e}"}
    