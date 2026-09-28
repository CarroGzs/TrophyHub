from werkzeug.security import generate_password_hash, check_password_hash
from app.database.database import get_db_connection

class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get_by_username(username):
        """
        Busca um usuário por username no banco usando cursor.
        PROTEÇÃO CONTRA SQL INJECTION: Uso da tupla (username,) com o marcador '?'.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # O cursor parametriza o valor de 'username', impedindo SQL Injection
        query = "SELECT id, username, email, password_hash FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        user_row = cursor.fetchone()
        
        # Sempre feche o cursor e a conexão após a operação
        cursor.close()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None

    @staticmethod
    def get_by_id(user_id):
        """
        Busca um usuário por ID.
        PROTEÇÃO CONTRA SQL INJECTION: Uso de tupla (user_id,) no parâmetro.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, username, email, password_hash FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        
        user_row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None

    @staticmethod
    def create(username, email, password):
        """
        Insere um novo usuário na tabela usando cursor.
        PROTEÇÃO CONTRA SQL INJECTION: Passagem de uma tupla com múltiplos parâmetros.
        """
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Padrão seguro com cursor e marcadores '?'
            query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (username, email, password_hash))
            
            # Confirma a transação
            conn.commit()
            
            # Obtém o ID gerado para a nova linha
            new_id = cursor.lastrowid
            
            return new_id
        except Exception as e:
            # Cancela as alterações em caso de erro (ex: username ou email duplicado)
            conn.rollback()
            raise e
        finally:
            # O bloco finally garante o fechamento dos recursos mesmo se ocorrer exceção
            cursor.close()
            conn.close()

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        """
        Verifica se a senha em texto puro corresponde ao hash armazenado no banco.
        """
        return check_password_hash(stored_password_hash, provided_password)