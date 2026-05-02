import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",   # ← your password
            database="ai_interviewer"
        )
        return connection
    except Error as e:
        print("Database connection error:", e)
        return None


# test connection
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("DB Connected")