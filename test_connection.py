import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jaskaran@cr7",
        database="bankmanagementsystem"
    )

    if conn.is_connected():
        print("✅ Connected to MySQL successfully!")
        conn.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
