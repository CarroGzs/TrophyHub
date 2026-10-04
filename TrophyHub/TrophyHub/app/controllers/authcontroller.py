from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usermodel import User
from app.middlewares.authmiddlewares import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../views')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validação de campos vazios
        if not username or not email or not password:
            flash('Preencha todos os campos para se cadastrar.', 'warning')
            return render_template('register.html')

        # Validação de senhas iguais
        if password != confirm_password:
            flash('As senhas digitadas não coincidem.', 'danger')
            return render_template('register.html')

        # Validação de usuário/email existente
        if User.get_by_username(username):
            flash('Este nome de usuário já está cadastrado.', 'danger')
            return render_template('register.html')

        if User.get_by_email(email):
            flash('Este e-mail já está associado a outra conta.', 'danger')
            return render_template('register.html')

        # Cadastro no banco SQLite via SQL puro
        try:
            User.create(username, email, password)
            flash('Conta criada com sucesso! Faça seu login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            flash('Ocorreu um erro interno ao criar a conta. Tente novamente.', 'danger')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user_data = User.get_by_username(username)

        if user_data and User.verify_password(user_data['password_hash'], password):
            session.clear()
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            flash(f'Bem-vindo de volta, {user_data["username"]}!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você encerrou sua sessão com sucesso.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/home')
@login_required
def home():
    return render_template('home.html', username=session.get('username'))