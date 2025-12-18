from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Asset, Collection, User
from . import db
from .forms import ProfileForm
from werkzeug.security import generate_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@routes.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for('auth.login'))

@routes.route('/assets')
@login_required
def asset_list():
    assets = Asset.query.all()
    return render_template('asset_list.html', assets=assets)
#my collection - quries with the user id to return all the assets from Collection table
@routes.route('/my_collection')
@login_required
def my_collection():
    collection = Collection.query.filter_by(user_id=current_user.id).all()
    return render_template('my_collection.html', collection=collection)

#function for adding assets to users collection
@routes.route('/collect/<int:asset_id>')
@login_required
def collect_asset(asset_id):
    existing = Collection.query.filter_by(user_id=current_user.id, asset_id=asset_id).first()
    if existing:
        flash("You already have this asset in your collection.", "info")
    else:
        new = Collection(user_id=current_user.id, asset_id=asset_id)
        db.session.add(new)
        db.session.commit()
        flash("asset added to your collection", "success")
    return redirect(url_for('routes.asset_list'))

#remove asset from my collection function - this is only allowed for admins using an if statement in the html
@routes.route('/remove/<int:asset_id>')
@login_required
def remove_asset(asset_id):
    entry = Collection.query.filter_by(user_id=current_user.id, asset_id=asset_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("asset removed from your collection.", "warning")
    else:
        flash("asset not found in your collection.", "danger")
    return redirect(url_for('routes.my_collection'))

#function allow users to go to their profile and edit details
@routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash("Username is already in use", "danger")
            return render_template('profile.html', form=form)

        current_user.username = form.username.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for('routes.profile'))

    return render_template('profile.html', form=form)


