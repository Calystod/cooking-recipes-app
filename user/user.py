from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database import helper
from werkzeug.security import generate_password_hash

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
    users = helper.get_multi('users', {})  # if this returns a user, then the email already exists in database
    return render_template('user/all_users.html', users=list(users))

@user_bp.route('/user/<id>/edit')
@login_required
def edit_user(id):
    user = helper.get('users', {'email': id})

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))

    return render_template('user/edit_user.html', user=user)

@user_bp.route('/user/<id>/edit', methods=['POST'])
@login_required
def edit_user_put(id):
    email = request.form.get('email')

    new_user = {'_id': id,
                'email': email,
                'name': request.form.get('name'),
                'password': generate_password_hash(request.form.get('password'), method='sha256')
                }
    user = helper.get('users', {'_id': id})

    # if this returns a user, then the email already exists in database
    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))

    user_id = helper.add('users', new_user)

    flash('User ' + user.name + ' edit.')
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

    user = helper.get('users', {'email': email})

    if user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('Email address already exists')
        return redirect(url_for('user.add_user'))

    new_user = {'email': email,
                'name': name,
                'password': generate_password_hash(password, method='sha256')
                }

    print(new_user)

    # add the new user to the database
    helper.add('users', new_user)

    flash('New user ' + name + ' add.')
    return redirect(url_for('user.add_user'))

@user_bp.route('/user/<id>/delete')
@login_required
def delete_user(email):
    user = helper.get('users', {'email': email})

    if not user:  # if a user is found, we want to redirect back to add_user page so user can try again
        flash('This user does\'t exist.')
        return redirect(url_for('user.index'))
    return render_template('user/delete_user.html', user=user)


@user_bp.route('/user/<id>/delete', methods=['POST'])
@login_required
def delete_user_post(email):
    helper.delete('users', {'email': email})

    return redirect(url_for('user.all_users'))
