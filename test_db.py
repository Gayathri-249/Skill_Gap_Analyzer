from db import get_connection

connection = None

try:
    connection = get_connection()
    print("MySQL connection successful!")
    print("Connected database:", connection.database)

except Exception as error:
    print("Database connection failed:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()