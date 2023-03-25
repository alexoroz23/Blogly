"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogly23"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_users():
    """Redirect to list of users"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """List all users"""
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    """Show form to add new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Add new user to database"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User '{first_name} {last_name}' added.")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details of a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')

    db.session.add(user)
    db.session.commit()

    flash(f"User '{user.first_name} {user.last_name}' edited.")
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User '{user.first_name} {user.last_name}' deleted.")
    return redirect('/users')

@app.errorhandler(404)
def not_found(error):
    """Show 404 error page"""
    return render_template('404.html'), 404
