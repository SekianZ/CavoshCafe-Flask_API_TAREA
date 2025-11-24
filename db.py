import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,     # cambia si usas 3307
        user="root",
        password="",
        database="CavoshCafe",
        autocommit=True   # 👈 OBLIGATORIO
    )
