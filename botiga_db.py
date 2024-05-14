from datetime import datetime
import json
import mysql.connector


class botiga_db:

    def __init__(self): # El metodo inicializa una conexion a la base de datos utilizando los parametros de configuracion proporcionados en un archivo JSON
        try:
            config = json.load(open("config.json"))
            self.conn = mysql.connector.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
            )
        except Exception as e:
            return {"status": -1, "message": f"Error de conexion:{e}"}

    def __del__(self):  # El metodo cierra la conexion cuando borra la instacia
        if self.conn:
            self.conn.close()

    def read_producte(self, id): # El metodo consulta la base de datos para obtener la informacion de un producto especiofico identificado por su ID
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product WHERE product_id = {id};")
            data = cur.fetchone()
            columns = [col[0] for col in cur.description]
            data_dict = dict(zip(columns, data))
            return data_dict
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def read_productes(self): # El metodo consulta la base de datos para obtener la informacion de todos los productos
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product;")
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]
            result = [dict(zip(columns, row)) for row in data]
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def create_producte(self, producte): # El metodo inserta un nuevo producto en la base de datos utilizando los datos proporcionados
        try:
            cur = self.conn.cursor()
            cur.execute(
                f"INSERT INTO product (name, description, company, price, units, subcategory_id) VALUES ('{producte['name']}', '{producte['description']}', '{producte['company']}', {producte['price']}, {producte['units']}, {producte['subcategory_id']});"
            )
            self.conn.commit()
            result = json.dumps({"status": "S'ha afegit correctement"})
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def create_productes(self, productes): # El metodo permite crear varios productos a la vez en la base de datos, por cada producto se llama al metodo "create_producte"
        results = []
        for producte in productes:
            result = self.create_producte(producte)
            results.append(result)
        return results

    def delete_producte(self, product_id: int): # El metodo actualiza el nombre de un producto en la base de datos segun el ID proporcionado
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM product WHERE product_id = {product_id}")
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando el producto: {e}")
            return False

    def update_producte(self, product_id: int, name: str): # El metodo hace una consulta que selecciona detalles específicos de los productos, incluyendo el nombre de la categoria, el nombre de la subcategoria, el nombre del producto, la marca del producto y el precio, utilizamos los INNER JOIN para combinar las tablas product, subcategory y category segun las primary key y foreing key que estan la base de datos
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                UPDATE product
                SET name = %s
                WHERE product_id = %s
                """,
                (name, product_id),
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error actualizando el nombre del producto: {e}")
            return False
        
    def read_productes_details(self):
        try:
            cur = self.conn.cursor(dictionary=True)
            cur.execute("""
                SELECT c.name AS category_name, sc.name AS subcategory_name, p.name AS product_name, p.company AS product_brand, p.price AS product_price
                FROM product p
                INNER JOIN subcategory sc ON p.subcategory_id = sc.subcategory_id
                INNER JOIN category c ON sc.category_id = c.category_id;
            """)
            data = cur.fetchall()
            return data
        except Exception as e:
            print(f"Error leyendo los productos: {e}")
            return []
