import json
import mysql.connector


def db_client():
    try:
        config = json.load(open("config.json"))
        return mysql.connector.connect(
            host = config["host"],
            port = config["port"],
            user = config["user"],
            password = config["password"],
            database = config["database"],
        )
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}


# conn = db_client()
# cur = conn.cursor()
# cur.execute("SHOW CREATE TABLE category;")
# data = cur.fetchall()
# for _ in data:
#     print(_)
