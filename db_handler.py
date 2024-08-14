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

def insert_article(title, summary, last_updated, tag):
    """Insert article data into the PostgreSQL table."""
    connection = None
    cursor = None
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**DB_PARAMS)
        cursor = connection.cursor()

        # Define the SQL INSERT query
        insert_query = sql.SQL("""
            INSERT INTO articles (title, summary, last_updated, tag)
            VALUES (%s, %s, %s, %s)
        """)

        # Execute the query
        cursor.execute(insert_query, (title, summary, last_updated, tag))

        # Commit the transaction
        connection.commit()

        print(f"Article '{title}' inserted successfully.")
    
    except psycopg2.Error as error:
        print(f"Error while inserting data into PostgreSQL: {error}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_articles(query):
    """Fetch articles from the PostgreSQL table and return as a DataFrame."""
    try:
        # Establish a connection to the database using a context manager
        with psycopg2.connect(**DB_PARAMS) as connection:
            with connection.cursor() as cursor:
                # Execute the query
                cursor.execute(query)
                
                # Fetch all rows from the executed query
                rows = cursor.fetchall()
                
                # Get column names from the cursor description
                colnames = [desc[0] for desc in cursor.description]
                
                # Create a DataFrame from the fetched data
                df = pd.DataFrame(rows, columns=colnames)
                
                return df
    
    except psycopg2.Error as error:
        print(f"Error while querying data from PostgreSQL: {error}")
        return None