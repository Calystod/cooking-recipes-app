from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sys import stderr
from werkzeug.security import generate_password_hash, check_password_hash
from main import db
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

@auth_bp.route('/add_user')
@login_required
def add_user():
    return render_template('auth/add_user.html')

@auth_bp.route('/add_user', methods=['POST'])
@login_required
def add_user_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if not email or not name or not password:
        flash('Some datas are missing')
        return redirect(url_for('auth.add_user'))

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.add_user'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('New user ' + name + ' add.')
    return redirect(url_for('auth.add_user'))


@auth_bp.route('/edit_user/<id>')
@login_required
def edit_user(id):
    user = User.query.filter_by(
        id=id).first()

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))

    return render_template('auth/edit_user.html', user=user)

@auth_bp.route('/edit_user/<id>', methods=['POST'])
@login_required
def edit_user_post(id):
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        id=id).first()  # if this returns a user, then the email already exists in database

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))

    if name:
        user.name = name
    if password:
        user.password = generate_password_hash(password, method='sha256')
    if email:
        user.email = email

    # edit user to the database
    db.session.commit()

    flash('User ' + name + ' edit.')
    return redirect(url_for('user.index'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.index'))
