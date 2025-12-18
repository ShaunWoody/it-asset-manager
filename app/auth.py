from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, login_manager
from flask_login import current_user
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__, url_prefix='/auth')

#gets the current userid and stores it in the flask session
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

#logs the user in, checks database for the user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        #check password and username - have to check hashed version of password as we hash it so it's not readable on the database
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

#function for registering a user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        #make sure we don't allow the same name as other users when registering
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username is already in use", "danger")
            return render_template('register.html', form=form)

  
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

#logout function
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('auth.login'))
