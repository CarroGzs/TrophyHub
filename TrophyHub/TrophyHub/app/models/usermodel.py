from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db_connection

class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get_by_username(username):
        """Busca um utilizador pelo username."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, username, email, password_hash FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        user_row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None

    @staticmethod
    def get_by_email(email):
        """Busca um utilizador pelo e-mail (para evitar duplicados)."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, username, email, password_hash FROM users WHERE email = ?"
        cursor.execute(query, (email,))
        user_row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None

    @staticmethod
    def create(username, email, password):
        """
        Cria um novo utilizador no banco SQLite.
        Proteção contra SQL Injection usando ? e envio em tupla.
        """
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (username, email, password_hash))
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password)