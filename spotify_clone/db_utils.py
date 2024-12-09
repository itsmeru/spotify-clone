from spotify_clone.services.db import execute_query

class DBUtils:
    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,))
        return result[0] if result else None
    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT id, username, email FROM users WHERE id = %s"
        result = execute_query(query, (user_id,))
        return result[0] if result else None
    @staticmethod
    def get_user_by_provider_id(provider: str, provider_id: str):
        query = "SELECT * FROM users WHERE provider = %s AND provider_id = %s"
        result = execute_query(query, (provider, provider_id))
        return result[0] if result else None
    @staticmethod
    def insert_data_to_users(email, username, hashed_password=None, provider=None, provider_id=None):
        query = """
        INSERT INTO users (email, username, hashed_password, provider, provider_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, email, username, created_at, provider
        """
        result = execute_query(query, (email, username, hashed_password, provider, provider_id))
        return result[0] if result else None