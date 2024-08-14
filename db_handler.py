import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_PARAMS)

def insert_article(title, summary, last_updated, tag):
    """Insert article data into the PostgreSQL table if it does not already exist."""
    
    # Check if the article already exists
    check_query = sql.SQL("""
        SELECT COUNT(*) FROM articles WHERE title = %s
    """)
    
    insert_query = sql.SQL("""
        INSERT INTO articles (title, summary, last_updated, tag)
        VALUES (%s, %s, %s, %s)
    """)

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Check if the article already exists
                cursor.execute(check_query, (title,))
                exists = cursor.fetchone()[0] > 0
                
                if not exists:
                    # Insert the article if it does not exist
                    cursor.execute(insert_query, (title, summary, last_updated, tag))
                    connection.commit()
                    print(f"Article '{title}' inserted successfully.")
                else:
                    print(f"Article '{title}' already exists in the database.")
    
    except psycopg2.Error as error:
        print(f"Error while inserting data into PostgreSQL: {error}")

def fetch_articles(query):
    """Fetch articles from the PostgreSQL table and return as a DataFrame."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]
                return pd.DataFrame(rows, columns=colnames)
    
    except psycopg2.Error as error:
        print(f"Error while querying data from PostgreSQL: {error}")
        return None
    
def delete_articles():
    """Delete all articles from the PostgreSQL table."""
    query = sql.SQL("DELETE FROM articles")
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                # reset the auto increment value
                cursor.execute("ALTER SEQUENCE articles_id_seq RESTART WITH 1")
                connection.commit()

        print("All articles deleted successfully.")
    
    except psycopg2.Error as error:
        print(f"Error while deleting data from PostgreSQL: {error}")
