import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    execute_query(query)

def get_db_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            database="spotify_db",
            user="spotify_user",
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor
        )
    except psycopg2.Error as e:
        print(f"Unable to connect to the database: {e}")
        raise


def execute_query(query, params=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query,params)
                conn.commit()
                try:
                    return cur.fetchall()
                except psycopg2.ProgrammingError :
                    return None
    except psycopg2.Error as e:
        print("connecting DB error", e)
    