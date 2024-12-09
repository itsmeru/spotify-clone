import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

connection_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="postgres",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    cursor_factory=RealDictCursor
)
def init_db():
    create_extension_query = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """

    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            hashed_password VARCHAR(255),  
            provider VARCHAR(50),          
            provider_id VARCHAR(255),    
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(provider, provider_id) 
        );
    """
    
    execute_query(create_extension_query)
    execute_query(create_table_query)

def get_db_connection():
    try:
        return connection_pool.getconn()
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

def close_pool():
    if connection_pool:
        connection_pool.closeall()
   
    