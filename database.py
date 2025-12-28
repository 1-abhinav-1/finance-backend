import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            category TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_expense(date, description, category, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (date, description, category, amount)
        VALUES (?, ?, ?, ?)
        """,
        (date, description, category, amount),
    )

    conn.commit()
    conn.close()


def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, description, category, amount FROM expenses")
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
