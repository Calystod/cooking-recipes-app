from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sys import stderr
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    print(user, file=stderr)
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    flash('Logged in successfully.')
    return redirect(url_for('user.profile'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.index'))
