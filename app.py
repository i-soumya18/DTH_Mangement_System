from flask import Flask, render_template, request, redirect, url_for, flash, session
from database_setup import check_credentials, signup_data, get_profile_data, update_user_data, add_channel, get_cart_data, delete_channel, clear_cart, store_purchased_channels, get_purchased_channels
from service import get_channel_data

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
    # Example channel ID (replace this with the actual channel ID you want to fetch)
    channel_id = "@NarendraModi"

    # Call the function to fetch channel data using the provided channel ID
    channel_data = get_channel_data(channel_id)

    if channel_data:
        # If channel data is successfully fetched, pass it to the service.html template
        return render_template('service.html', channel_data=channel_data)
    else:
        # If channel data retrieval fails, return an error message or handle it accordingly
        return "Failed to fetch YouTube channel data. Please try again later."



@app.route('/profile')
def profile():
    email = session.get('email')
    if email:
        user_data = get_profile_data(email)
        if user_data:
            purchased_channels = get_purchased_channels(email)
            return render_template('profile.html', user=user_data, purchased_channels=purchased_channels)
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

@app.route('/add_channel', methods=['POST'])
def add_channel_to_cart():
    email = session.get('email')
    if email:
        channel_id = request.form.get('channel_id')
        channel_data = get_channel_data(channel_id)
        if channel_data:
            add_channel(email, channel_data)
            flash('Channel added to cart successfully!', 'success')
        else:
            flash('Failed to add channel to cart. Channel data not found.', 'error')
    else:
        flash('User not logged in!', 'error')
    return redirect(url_for('service'))


@app.route('/delete_channel', methods=['POST'])
def delete_channel_from_cart():
    email = session.get('email')
    channel_id = request.form.get('channel_id')
    if email and channel_id:
        delete_channel(email, channel_id)
        flash('Channel deleted from cart successfully!', 'success')
    else:
        flash('Channel not found!', 'error')
    return redirect(url_for('cart'))


@app.route('/purchase', methods=['POST'])
def purchase_channels():
    email = session.get('email')
    if email:
        cart_data = get_cart_data(email)
        if cart_data:
            store_purchased_channels(email, cart_data)
            clear_cart(email)
            flash('Channels purchased successfully!', 'success')
        else:
            flash('No channels in the cart to purchase!', 'warning')
    else:
        flash('User not logged in!', 'error')
    return redirect(url_for('cart'))


# Route to display the cart
@app.route('/cart')
def cart():
    # Retrieve the logged-in user's email from the session
    email = session.get('email')

    if email:
        # Get the cart data for the logged-in user
        cart_data = get_cart_data(email)

        # Render the cart template with cart data
        return render_template('cart.html', cart_data=cart_data)
    else:
        # If user is not logged in, redirect to the login page
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'abcdefghijklmnopqrswxyz'
    app.run(host='0.0.0.0', port=8080)
