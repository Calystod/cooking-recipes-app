from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import User
from werkzeug.security import generate_password_hash
from main import db

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/')
def index():
    return render_template('index.html')


@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', name=current_user.name)

@user_bp.route('/users')
@login_required
def all_users():
    users = User.query.all()  # if this returns a user, then the email already exists in database
    return render_template('user/all_users.html', users=users)

@user_bp.route('/user/<id>/edit')
@login_required
def edit_user(id):
    user = User.query.filter_by(
        id=id).first()

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))

    return render_template('user/edit_user.html', user=user)

@user_bp.route('/user/<id>/edit', methods=['POST'])
@login_required
def edit_user_put(id):
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

@user_bp.route('/user')
@login_required
def add_user():
    return render_template('user/add_user.html')

@user_bp.route('/user', methods=['POST'])
@login_required
def add_user_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if not email or not name or not password:
        flash('Some datas are missing')
        return redirect(url_for('user.add_user'))

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('Email address already exists')
        return redirect(url_for('user.add_user'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('New user ' + name + ' add.')
    return redirect(url_for('user.add_user'))

@user_bp.route('/user/<id>/delete')
@login_required
def delete_user(id):
    user = User.query.filter_by(
        id=id).first()

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))
    return render_template('user/delete_user.html', user=user)

@user_bp.route('/user/<id>/delete', methods=['POST'])
@login_required
def delete_user_post(id):
    user = User.query.filter_by(
        id=id).first()

    User.query.filter_by(id=id).delete()
    db.session.commit()

    flash('User delete.')
    return redirect(url_for('user.all_users'))
