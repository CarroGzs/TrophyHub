# app/controllers/main_controller.py
from flask import Blueprint, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('auth.home'))
    return redirect(url_for('auth.login'))