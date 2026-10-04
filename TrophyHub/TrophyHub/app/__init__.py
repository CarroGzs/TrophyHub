import os
from flask import Flask
from app.database import init_db

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='statics')
    app.config['SECRET_KEY'] = 'chave-secreta-trophyhub-dev'

    # Cria o arquivo do banco e a tabela de usuários na primeira execução
    init_db()

    # Registro dos Blueprints
    from app.controllers.authcontroller import auth_bp
    from app.controllers.maincontroller import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app