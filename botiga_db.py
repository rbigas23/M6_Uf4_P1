import json
import mysql.connector


class botiga_db:

    def __init__(self):
        try:
            config = json.load(open("config.json"))
            self.conn = mysql.connector.connect(
                host = config["host"],
                port = config["port"],
                user = config["user"],
                password = config["password"],
                database = config["database"],
            )
        except Exception as e:
            return{"status": -1, "message":f"Error de conexion:{e}"}
    
    def __del__(self):  # Tanca la connexió quan s'esborra la instància
        if self.conn:
            self.conn.close()

    def read_producte(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product WHERE product_id = {id};")
            data = cur.fetchone()
            columns = [col[0] for col in cur.description]
            data_dict = dict(zip(columns, data))
            return data_dict
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def read_productes(self):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product;")
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]
            result = [dict(zip(columns, row)) for row in data]
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def create_producte(self, producte):
        try:
            cur = self.conn.cursor()
            cur.execute(f"INSERT INTO product (name, description, company, price, units, subcategory_id) VALUES ('{producte['name']}', '{producte['description']}', '{producte['company']}', {producte['price']}, {producte['units']}, {producte['subcategory_id']});")
            self.conn.commit()
            result = json.dumps({"status": "S'ha afegit correctement"})
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def create_productes(productes):
        pass

    def update_producte(id, producte):
        pass

    def delete_producte(id):
        pass
    