# db.py
import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaskaran@cr7",  # Your real password
            database="bankmanagementsystem"
        )
        return connection
    except mysql.connector.Error as err:
        print("Connection error:", err)
        return None
