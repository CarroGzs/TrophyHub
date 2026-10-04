from app.models.usermodel import User

def populate():
    print("Inserindo usuários de teste no SQLite...")
    try:
        if not User.get_by_username('admin'):
            User.create('admin', 'admin@trophyhub.com', '123')
            print("Usuário 'admin' criado com sucesso!")

        if not User.get_by_username('jogador1'):
            User.create('jogador1', 'jogador1@trophyhub.com', 'abc')
            print("Usuário 'jogador1' criado com sucesso!")
            
    except Exception as e:
        print(f"Erro ao inserir usuários: {e}")

if __name__ == '__main__':
    populate()