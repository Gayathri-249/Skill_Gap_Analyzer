
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def test_mysql_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=5,
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()

        assert result[0] == "skill_gap_analyzer"
        cursor.close()
    finally:
        connection.close()
