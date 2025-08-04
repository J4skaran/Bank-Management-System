# db.py
import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alpha",
            password="Jask7",  
            database="bankmanagementsystem"
        )
        return connection
    except mysql.connector.Error as err:
        print("Connection error:", err)
        return None
