import csv
import datetime
import json
import mysql.connector


class botiga_db:

    def __init__(self):  # Inicialitza una conexió amb la base de dades utilizant els paràmetres de configuració proporcionats al arxiu JSON corresponent
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

    def __del__(self):  # Tanca la connexió quan s'esborra la instància
        if self.conn:
            self.conn.close()

    # MÈTODES CRUD

    def create_producte(self, product_data):  # Crea un producte a la taula amb la informació especificada i retorna un missatge indicant si s'ha cerat correctament
        try:
            cur = self.conn.cursor()
            cur.execute(
                f"INSERT INTO product (name, description, company, price, units, subcategory_id) VALUES ('{product_data['name']}', '{product_data['description']}', '{product_data['company']}', {product_data['price']}, {product_data['units']}, {product_data['subcategory_id']});"
            )
            self.conn.commit()
            result = json.dumps({"status": "S'ha afegit correctement"})
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def create_productes(self, productes):  # El método permite crear varios productos a la vez en la base de datos, por cada producto se llama al método "create_producte"
        results = []
        for producte in productes:
            result = self.create_producte(producte)
            results.append(result)
        return results

    def read_producte(self, id):  # Retorna la informació d'un producte amb una id específica o el missatge d'error corresponent
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product WHERE product_id = {id};")
            data = cur.fetchone()
            columns = [col[0] for col in cur.description]
            data_dict = dict(zip(columns, data))
            return data_dict
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}

    def read_productes(self):  # Retorna la informació de tots els productes de la taula o el missatge d'error corresponent
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM product;")
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]
            result = [dict(zip(columns, row)) for row in data]
            return result
        except Exception as e:
            return {"status": -1, "message": f"Error llegint el producte: {e}"}
        
    def read_productes_details(self):  # Retorna la informació de tots els productes de la taula, incloent els noms de la categoria i la subcategoria
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

    def update_producte(self, product_id: int, name: str): # El método hace una consulta que selecciona detalles específicos de los productos, incluyendo el nombre de la categoria, el nombre de la subcategoria, el nombre del producto, la marca del producto y el precio, utilizamos los INNER JOIN para combinar las tablas product, subcategory y category segun las primary key y foreing key que estan la base de datos
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
        
    def delete_producte(self, product_id: int): # El método actualiza el nombre de un producto en la base de datos segun el ID proporcionado
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM product WHERE product_id = {product_id}")
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando el producto: {e}")
            return False

    # MÈTODES PER A CARREGAR PRODUCTES AMB CSV

    def load_products(self, filename):  # Carrega tots els productes continguts en el fitxer csv especificat
        with open(f"{filename}.csv") as csv_file:
            products = csv.DictReader(csv_file)  # Fem servir la llibreria csv per llegir el contingut

            for product in products:  # Per cada producte es processen els diferents grups de dades i s'insereixen/actualitzen els registres corresponents

                category_dict = {'category_id':product['id_categoria'], 'name':product['nom_categoria']}
                self.process_item(category_dict, "category")

                subcategory_dict = {'subcategory_id':product['id_subcategoria'], 'name':product['nom_subcategoria'], 'category_id':product['id_categoria']}
                self.process_item(subcategory_dict, "subcategory")

                product_dict = {'product_id':product['id_producto'], 'name':product['nom_producto'], 'description':product['descripcion_producto'], 'company':product['companyia'], 'price':product['precio'], 'units':product['unidades'], 'subcategory_id':product['id_subcategoria']}
                self.process_item(product_dict, "product")

    def exist(self, table, id):  # Comproba si existeix un registre amb una id determinada a la taula especificada
        cur = self.conn.cursor()
        cur.execute(f"SELECT 1 FROM {table} WHERE {table}_id = {id};")
        data = cur.fetchone()
        return data is not None
    
    def create_item(self, table, data):  # Insereix les dades d'un ítem (categoria, subcategoria o producte) a la taula especificada
        cur = self.conn.cursor()
        columns = ", ".join(data.keys())
        values = ", ".join("\"" + value + "\"" if isinstance(value, str) else value for value in data.values())
        cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        self.conn.commit()

    def update_item (self, table, name, id):  # Actualitza el nom i la id d'un ítem (categoria, subcategoria o producte) a la taula especificada
        cur = self.conn.cursor()
        cur.execute(f"UPDATE {table} SET name = '{name}', updated_at = '{datetime.datetime.now()}' WHERE {table}_id = {id};")
        self.conn.commit()

    """El mètode següent s'encarrega de processar les dades d'una categoria, una subcategoria o un producte
       (actualitza o insereix les dades segons si l'element ja existeix o no)"""

    def process_item(self, item_dict, item_name):  
        id = item_dict[f'{item_name}_id']
        if self.exist(item_name, id):
            self.update_item(item_name, item_dict['name'], id)
        else:
            item_dict.pop(f'{item_name}_id')  # Eliminem la id ja que no la necessitem per fer la inserció a la base de dades
            self.create_item(item_name, item_dict)
