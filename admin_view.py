from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt

admin_blueprint = Blueprint('admin', __name__)

bcrypt = Bcrypt()

# Dummy data for demonstration (Replace with actual database implementation)
admins = []

@admin_blueprint.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        if not admins:
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            admins.append({'username': username, 'password': hashed_password})
            flash('Admin registration successful. You can now sign in as an admin.', 'success')
            return redirect(url_for('admin.admin_signin'))
        else:
            flash('Admin already registered. Please sign in.', 'error')
            return redirect(url_for('admin.admin_signin'))
    return render_template('admin_signup.html')

@admin_blueprint.route('/admin/signin', methods=['GET', 'POST'])
def admin_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for admin in admins:
            if admin['username'] == username and bcrypt.check_password_hash(admin['password'], password):
                session['username'] = username
                return "Admin signin successful"
        flash('Invalid username or password', 'error')
    return render_template('admin_signin.html')

@admin_blueprint.route('/admin/create_admin', methods=['GET', 'POST'])
def create_admin():
    if 'username' in session:
        if request.method == 'POST':
            # Add logic to create new admin account here
            return "New admin account created successfully"
        return render_template('create_admin.html')
    else:
        return redirect(url_for('admin.admin_signin'))
