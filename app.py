from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Function to check if the provided email and password match any stored credentials
def check_credentials(email, password):
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)
            for user in credentials:
                if user['email'] == email and user['password'] == password:
                    return True
    return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home1():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_data():
    # Get data from the signup form
    name = request.form.get('yourName')
    email = request.form.get('exampleInputEmail1')
    password = request.form.get('exampleInputPassword1')

    # Create dictionary for user credentials
    user_data = {
        'name': name,
        'email': email,
        'password': password
    }

    # Check if the credentials file exists
    if os.path.exists('credentials.json'):
        # Load existing credentials from file
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)
    else:
        # If the file doesn't exist, create an empty list
        credentials = []

    # Add new user data to credentials
    credentials.append(user_data)

    # Write updated credentials to file
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file, indent=4)

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login_user():
    # Get email and password from the login form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if provided credentials match any stored credentials
    if check_credentials(email, password):
        # Redirect to the profile page upon successful login
        return redirect(url_for('home'))
    else:
        # Redirect back to the login page with an error message
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
