# apps/authentication/routes.py

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from apps import login_manager, db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass
from sqlalchemy.exc import IntegrityError
from flask import jsonify

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('home_blueprint.index'))
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html', msg='Username already registered', success=False, form=create_account_form)
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html', msg='Email already registered', success=False, form=create_account_form)
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()
        logout_user()
        return render_template('accounts/register.html', msg='Account created successfully.', success=True, form=create_account_form)
    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

@blueprint.route('/tables.html')
def tables():
    users = Users.query.all()
    return render_template('home/tables.html', users=users)

@blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    create_account_form = CreateAccountForm(request.form)
    if request.method == 'POST' and create_account_form.validate():
        existing_user = Users.query.filter_by(email=create_account_form.email.data).first()
        if existing_user:
            error_msg = "Email already registered."
            return render_template('accounts/add_user.html', form=create_account_form, error_msg=error_msg)
        try:
            new_user = Users(
                username=create_account_form.username.data,
                email=create_account_form.email.data,
                password=create_account_form.password.data,
                salary=create_account_form.salary.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('authentication_blueprint.tables'))
        except IntegrityError as e:
            db.session.rollback()
            error_msg = "Error occurred while adding user. Please try again."
            return render_template('accounts/add_user.html', form=create_account_form, error_msg=error_msg)
    return render_template('accounts/add_user.html', form=create_account_form)

@blueprint.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return redirect(url_for('authentication_blueprint.tables'))
    edit_form = CreateAccountForm(request.form, obj=user)
    if request.method == 'POST' and edit_form.validate():
        user.username = edit_form.username.data
        user.email = edit_form.email.data
        user.salary = edit_form.salary.data
        db.session.commit()
        return redirect(url_for('authentication_blueprint.tables'))
    return render_template('accounts/edit_user.html', user=user, form=edit_form)

@blueprint.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return redirect(url_for('authentication_blueprint.tables'))
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('authentication_blueprint.tables'))
    return render_template('accounts/delete_user.html', user=user)

@blueprint.route('/salaries', methods=['GET'])
def get_salaries():
    salaries = [user.salary for user in Users.query.all()]
    return jsonify(salaries)
