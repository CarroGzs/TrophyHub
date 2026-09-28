import sqlite3
import os

# Caminho absoluto para garantir que o banco fique na raiz do projeto
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trophyhub.db')

def get_db_connection():
    """
    Cria e retorna uma conexão NOVA e INDEPENDENTE com o SQLite.
    Cada chamada gera uma instância de conexão separada.
    """
    conn = sqlite3.connect(DB_PATH)
    # Permite acessar colunas pelo nome: row['username']
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa o banco de dados criando a tabela de usuários se não existir.
    Utiliza sua própria conexão independente.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close() # Fecha a conexão de inicialização