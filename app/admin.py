from flask import Blueprint, render_template, redirect, url_for, request, flash,abort
from flask_login import login_required, current_user
from .models import User, Collection, Asset
from . import db
from .forms import AddassetForm, EditUserForm, EditassetForm
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

#this function allows us to call it each time we go down an admin route to make sure it the user is a admin user (similar to login_required)
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash("You don't have the required permissions", "danger")
            return redirect(url_for('routes.dashboard'))
        return f(*args, **kwargs)
    return wrapper

@admin.route('/')
@login_required
@admin_required
def admin_dashboard():
    #in the admin dashboard we see all of the master assets listed (quires our database model for all assets and then passes it into the dashboard template)
    assets = Asset.query.all()
    return render_template('admin/dashboard.html', assets=assets)

@admin.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
#function to add assets to the master list (adds record in database)
def add_asset():
    form = AddassetForm()
    if form.validate_on_submit():
        new_asset = Asset(
            name=form.name.data,
            asset_tag=form.asset_tag.data,
            asset_type=form.asset_type.data,
            location=form.location.data
        )
        db.session.add(new_asset)
        db.session.commit()
        flash("asset added successfully", "success")
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_asset.html', form=form)

@admin.route('/delete/<int:asset_id>')
@login_required
@admin_required
#function to delete assets from master list (deletes a record in database)
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash("asset deleted.", "warning") #from flash libary, these act as alerts with message coming first and alert type second
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/edit/<int:asset_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    form = EditassetForm(obj=asset)

    if form.validate_on_submit():
        asset.name = form.name.data
        asset.asset_tag = form.asset_tag.data
        asset.asset_type = form.asset_type.data
        asset.location = form.location.data
        db.session.commit()
        flash('asset updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_asset.html', form=form, asset=asset)

@admin.route('/users')
@login_required
def user_list():
    if current_user.role != 'admin':
        flash("You don't have the required permissions", "danger")
        return redirect(url_for('routes.dashboard'))

    users = User.query.all()
    return render_template('admin/user_list.html', users=users)

#function to allow admins to edit user details
@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash("You don't have the required permissions", "danger")
        return redirect(url_for('routes.dashboard'))

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.id != user.id:
            flash("Username is already in use", "danger")
            return render_template('admin/edit_user.html', user=user, form=form)

        user.username = form.username.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('admin.user_list'))

    return render_template('admin/edit_user.html', user=user, form=form)

#function to allow admins to delete users
@admin.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("You don't have the required permissions", "danger")
        return redirect(url_for('routes.dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You can't delete your own account.", "warning")
        return redirect(url_for('admin.user_list'))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin.user_list'))

#function to promote users to admin
@admin.route('/promote/<int:user_id>', methods=['GET', 'POST'])
@login_required
def promote_user(user_id):
    if current_user.role != 'admin':
        flash("You don't have the required permissions", "danger")
        return redirect(url_for('routes.dashboard'))

    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        user.role = 'admin'
        db.session.commit()
        flash(f"{user.username} has been promoted to admin.", "success")
    else:
        flash(f"{user.username} is already an admin.", "info")

    return redirect(url_for('admin.user_list'))

@admin.route('/collections')
@login_required
def all_collections():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin/all_collections.html', users=users)

#function to see users collections as admin
@admin.route('/collections/<int:user_id>')
@login_required
def view_user_collection(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    assets = [c.asset for c in Collection.query.filter_by(user_id=user_id).all()]
    all_assets = Asset.query.all()
    return render_template('admin/user_collection.html', user=user, assets=assets, all_assets=all_assets)

#function to remove assets from user collections
@admin.route('/collections/<int:user_id>/remove/<int:asset_id>')
@login_required
def remove_asset(user_id, asset_id):
    if current_user.role != 'admin':
        abort(403)
    entry = Collection.query.filter_by(user_id=user_id, asset_id=asset_id).first() # have to query the user id and asset id on colelctions
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("asset has been removed from user collection.")
    return redirect(url_for('admin.view_user_collection', user_id=user_id))

#function to add assets to a user collection
@admin.route('/collections/<int:user_id>/add_asset/<int:asset_id>', methods=['POST'])
@login_required
def add_asset_user(user_id, asset_id):
    if current_user.role != 'admin':
        abort(403)

    existing = Collection.query.filter_by(user_id=user_id, asset_id=asset_id).first()
    if not existing:
        new = Collection(user_id=user_id, asset_id=asset_id)
        db.session.add(new)
        db.session.commit()
        flash("asset added to user's collection", "success")
    else:
        flash("User already has this asset.", "info")

    return redirect(url_for('admin.view_user_collection', user_id=user_id))

