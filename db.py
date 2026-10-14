import json
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# Connect to the MySQL database
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "skill_gap_analyzer"),
    )


# Save one skill-gap analysis
def save_analysis(
    resume_filename,
    target_role,
    required_skills,
    matched_skills,
    missing_skills,
    coverage_percentage,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO analyses (
                resume_filename,
                target_role,
                required_skills,
                matched_skills,
                missing_skills,
                coverage_percentage
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            resume_filename,
            target_role,
            json.dumps(required_skills),
            json.dumps(matched_skills),
            json.dumps(missing_skills),
            coverage_percentage,
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except mysql.connector.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


# Retrieve recent analysis records
def get_recent_analyses(limit=20):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                resume_filename,
                target_role,
                required_skills,
                matched_skills,
                missing_skills,
                coverage_percentage,
                created_at
            FROM analyses
            ORDER BY created_at DESC
            LIMIT %s
        """

        cursor.execute(query, (limit,))
        records = cursor.fetchall()

        # Convert JSON columns into Python lists
        for record in records:
            for column in (
                "required_skills",
                "matched_skills",
                "missing_skills",
            ):
                value = record[column]

                if isinstance(value, str):
                    record[column] = json.loads(value)

        return records

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()