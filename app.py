from flask import Flask, render_template, request, redirect, url_for, flash, session
from database_setup import check_credentials, signup_data, get_profile_data, update_user_data,add_channel, get_cart_data, delete_channel, clear_cart, store_purchased_channels, get_purchased_channels
from service import get_channel_data
from database_setup import add_channel_to_db, connect_to_database, get_all_channels

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
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Check if there are any channels in the database
    channels = get_all_channels(cursor)
    if channels:
        # If channels exist, fetch all channel data
        return render_template('service.html', channels=channels)
    else:
        # If no channels exist, display a message
        return render_template('service.html', message="Start browsing channels")

    cursor.close()
    connection.close()



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

@app.route('/search_channel', methods=['POST'])
def search_channel():
    if request.method == 'POST':
        channel_name = request.form.get('channel_name')
        if channel_name:
            channel_data = get_channel_data(channel_name)
            if channel_data:
                # Add the fetched channel data to the database
                add_channel_to_db(channel_data)
                flash('Channel data fetched and stored successfully!', 'success')
            else:
                flash('Failed to fetch channel data. Please try again later.', 'error')
        else:
            flash('Please provide a channel name.', 'error')
        return redirect(url_for('service'))


'''@app.route('/add_channel', methods=['POST'])
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
    return redirect(url_for('service'))'''


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

from flask import session

@app.route('/add_channel', methods=['POST'])
def add_to_cart():
    # Check if the user is logged in
    email = session.get('email')
    if not email:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    if request.method == 'POST':
        # Extract form data
        channel_id = request.form['channel_id']
        channel_title = request.form['channel_name']
        channel_price = request.form['channel_price']
        email = session.get('email')
        print(channel_id, channel_title, channel_price, email)
        #channel_url = request.form['channel_url']

        # Add channel to cart table
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "INSERT INTO cart (email, channel_id, channel_title, channel_price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (email, channel_id, channel_title, channel_price))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Channel added to cart successfully!', 'success')
            return redirect(url_for('service'))  # Redirect to the page where channels are displayed
        except Exception as e:
            print("Error adding channel to cart:", e)
            flash('An error occurred while adding the channel to the cart.', 'error')
            return redirect(url_for('service'))  # Redirect to the page where channels are displayed

# write a function to add user selected channel to purchased_channels table when user clicks on purchase button in cart.html and simultaneously delete the particular channel from cart table and display a message "Channel purchased successfully" in cart.html page after the channel is purchased successfully.
@app.route('/purchase_channel', methods=['POST'])
def purchase_channel():
    # Check if the user is logged in
    email = session.get('email')
    if not email:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract form data
        channel_id = request.form['channel_id']
        channel_title = request.form['channel_name']
        channel_price = request.form['channel_price']
        email = session.get('email')

        # Add channel to purchased_channels table
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "INSERT INTO purchased_channels (email, channel_id, channel_title, channel_price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (email, channel_id, channel_title, channel_price))
            connection.commit()
            cursor.close()
            connection.close()

            # Delete the channel from the cart table
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "DELETE FROM cart WHERE email = %s AND channel_id = %s"
            cursor.execute(query, (email, channel_id))
            connection.commit()
            cursor.close()
            connection.close()

            flash('Channel purchased successfully!', 'success')
            return redirect(url_for('cart'))
        except Exception as e:
            print("Error purchasing channel:", e)
            flash('An error occurred while purchasing the channel.', 'error')
            return redirect(url_for('cart'))

@app.route('/delete_channel', methods=['POST'])
def delete_channel():
    # Check if the user is logged in
    email = session.get('email')
    if not email:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract form data
        channel_id = request.form['channel_id']

        # Delete the channel from the cart table
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "DELETE FROM cart WHERE email = %s AND channel_id = %s"
            cursor.execute(query, (email, channel_id))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Channel deleted from cart successfully!', 'success')
            return redirect(url_for('cart'))
        except Exception as e:
            print("Error deleting channel from cart:", e)
            flash('An error occurred while deleting the channel from the cart.', 'error')
            return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    # Check if the user is logged in
    email = session.get('email')
    if not email:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Clear the cart for the user
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "DELETE FROM cart WHERE email = %s"
            cursor.execute(query, (email,))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Cart cleared successfully!', 'success')
            return redirect(url_for('cart'))
        except Exception as e:
            print("Error clearing cart:", e)
            flash('An error occurred while clearing the cart.', 'error')
            return redirect(url_for('cart'))






if __name__ == "__main__":
    app.secret_key = 'abcdefghijklmnopqrswxyz'
    app.run(host='0.0.0.0', port=8080)