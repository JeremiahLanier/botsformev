# db/database.py

import psycopg2
from psycopg2.extras import RealDictCursor


def connect_db():
    """Establish a database connection using psycopg2."""
    connection = psycopg2.connect(
        dbname='trading_bot',
        user='bot_user',
        password='your_password',
        host='localhost'
    )
    return connection


def create_tables():
    """Create database tables based on schema.sql file."""
    connection = connect_db()
    cursor = connection.cursor()
    with open('db/schema.sql', 'r') as f:
        cursor.execute(f.read())
    connection.commit()
    cursor.close()
    connection.close()


def execute_query(query, args=None):
    """Execute a single query."""
    connection = connect_db()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, args)
        connection.commit()
        if cursor.description:
            return cursor.fetchall()  # Return data for SELECT queries
    finally:
        cursor.close()
        connection.close()
