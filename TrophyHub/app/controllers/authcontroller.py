from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usermodel import User
from app.middlewares.authmiddlewares import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../views')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Busca no banco SQLite via SQL puro
        user_data = User.get_by_username(username)

        if user_data and User.verify_password(user_data['password_hash'], password):
            session.clear()
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/home')
@login_required
def home():
    return render_template('home.html', username=session.get('username'))