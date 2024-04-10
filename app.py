from flask import Flask, render_template, request, redirect, url_for, flash
from database_setup import check_credentials, signup_data, get_profile_data

app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrswxyz'

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
    user_data = get_profile_data()
    return render_template('profile.html', user=user_data)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    result = signup_data(request.form)
    if result:
        return redirect(url_for('home'))
    else:
        flash('User already exists with the same email!', 'error')
        return redirect(url_for('signup'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    if check_credentials(email, password):
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Add a secret key for session management
    app.run(host='0.0.0.0', port=8080)
