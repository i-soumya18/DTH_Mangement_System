from flask import Flask, render_template, request, redirect, url_for, flash, session
from database_setup import check_credentials, signup_data, get_profile_data, update_user_data



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

#@app.route('/profile')
#def profile1():
#    return render_template('profile.html')

@app.route('/profile')
def profile():
    # Retrieve user's email from session
    email = session.get('email')

    if email:
        # Fetch user's data from database using email
        user_data = get_profile_data(email)
        if user_data:
            # Pass user's data to render_template function
            return render_template('profile.html', user=user_data)
        else:
            return 'User data not found'
    else:
        return redirect(url_for('login'))

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
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    if check_credentials(email, password):
        # Store user's email in session upon successful login
        session['email'] = email
        return redirect(url_for('profile'))
    else:
        # Redirect back to login page with error message
        return redirect(url_for('login'))
# Route for logout
@app.route('/logout')
def logout():
    # Clear the user's session
    session.pop('email', None)
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    form_data = request.form
    # Call the update_user_data function from database_setup.py
    update_result = update_user_data(form_data)
    if update_result:
        flash('Profile updated successfully!', 'success')
    else:
        flash('Failed to update profile!', 'error')
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.secret_key = 'abcdefghijklmnopqrswxyz'  # Add a secret key for session management
    app.run(host='0.0.0.0', port=8080)
