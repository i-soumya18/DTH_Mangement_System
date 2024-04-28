import mysql.connector

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="soumya",
        database="dth_data"
    )




# Function to check if the provided email and password match any stored credentials in the database
def check_credentials(email, password):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

# Function to insert user data into the database
def signup_data(form_data):
    name = form_data.get('yourName')
    email = form_data.get('exampleInputEmail1')
    password = form_data.get('exampleInputPassword1')
    phone_number = form_data.get('exampleInputPhoneNumber')
    street = form_data.get('exampleInputStreet')
    state = form_data.get('exampleInputState')
    city = form_data.get('exampleInputCity')
    zip_code = form_data.get('exampleInputZipCode')

    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email, password, phone_number, street, state, city, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, password, phone_number, street, state, city, zip_code))
    connection.commit()
    cursor.close()
    connection.close()

# Function to retrieve user profile data from the database
def get_profile_data(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_data

# Function to check if the email already exists in the database
def check_email_exists(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

# Function to delete user from the database based on email
def delete_user(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    connection.commit()
    cursor.close()
    connection.close()

#Function to update user data in the database through profile page
def update_user_data(form_data):
    name = form_data.get('yourName')
    email = form_data.get('exampleInputEmail1')
    #password = form_data.get('exampleInputPassword1')
    phone_number = form_data.get('exampleInputPhoneNumber')
    street = form_data.get('exampleInputStreet')
    state = form_data.get('exampleInputState')
    city = form_data.get('exampleInputCity')
    zip_code = form_data.get('exampleInputZipCode')

    connection = connect_to_database()
    cursor = connection.cursor()
    query = "UPDATE users SET name = %s, phone_number = %s, street = %s, state = %s, city = %s, zip_code = %s WHERE email = %s"
    cursor.execute(query, (name, phone_number, street, state, city, zip_code, email))
    connection.commit()
    cursor.close()
    connection.close()
    return True

#Function to retrieve all the users from the database
def get_all_users():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

# Function to add channel to the cart from channel table respective to the user
def add_channel(email, channel_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM channels WHERE channel_id = %s"
    cursor.execute(query, (channel_id,))
    channel_data = cursor.fetchone()
    if channel_data:
        query = "INSERT INTO cart (email, channel_id, channel_title, channel_price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, channel_data[0], channel_data[1], channel_data[2]))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    else:
        return False




# Function to get cart data for the user
def get_cart_data(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM cart WHERE email = %s"
    cursor.execute(query, (email,))
    cart_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return cart_data

# Function to delete channel from the cart
def delete_channel(email, channel_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "DELETE FROM cart WHERE email = %s AND channel_id = %s"
    cursor.execute(query, (email, channel_id))
    connection.commit()
    cursor.close()
    connection.close()

# Function to store purchased channels in the database
def store_purchased_channels(email, channels):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO purchased_channels (email, channel_id, channel_title, channel_price) VALUES (%s, %s, %s, %s)"
    for channel in channels:
        cursor.execute(query, (email, channel['channel_id'], channel['channel_title'], channel['channel_price']))
    connection.commit()
    cursor.close()
    connection.close()

def clear_cart(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "DELETE FROM cart WHERE email = %s"
    cursor.execute(query, (email,))
    connection.commit()
    cursor.close()
    connection.close()

# Function to retrieve purchased channels for a user
def get_purchased_channels(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM cart WHERE email = %s"
    cursor.execute(query, (email,))
    purchased_channels = cursor.fetchall()
    cursor.close()
    connection.close()
    return purchased_channels

# Function to add channel to the database
def add_channel_to_db(channel_data):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Check if the channel already exists in the database
        query = "SELECT * FROM channels WHERE channel_id = %s"
        cursor.execute(query, (channel_data['channel_id'],))
        existing_channel = cursor.fetchone()

        if existing_channel:
            # Channel already exists, you can choose to update it or skip
            pass
        else:
            # Insert the channel into the database
            query = "INSERT INTO channels (channel_id, channel_name, channel_price, channel_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (channel_data['channel_id'], channel_data['channel_name'], channel_data['channel_price'], channel_data['channel_url']))
            connection.commit()

        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Error adding channel to database:", error)


def get_all_channels(cursor):
    query = "SELECT * FROM channels"
    cursor.execute(query)
    channels = cursor.fetchall()
    return channels

# write a function to add user selected channel from cart to another new table purchased_channels
def add_channel_to_purchased_channels(email, channel_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM cart WHERE email = %s AND channel_id = %s"
    cursor.execute(query, (email, channel_id))
    channel_data = cursor.fetchone()
    if channel_data:
        query = "INSERT INTO purchased_channels (email, channel_id, channel_title) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, channel_data[1], channel_data[2]))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    else:
        return False

# Function to get all the purchased channels for a user
def get_purchased_channels(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM purchased_channels WHERE email = %s"
    cursor.execute(query, (email,))
    purchased_channels = cursor.fetchall()
    cursor.close()
    connection.close()
    return purchased_channels


'''def get_purchased_channels(email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT channel_id, channel_title, channel_price FROM purchased_channels WHERE email = %s"
    cursor.execute(query, (email,))
    purchased_channels = cursor.fetchall()
    cursor.close()
    connection.close()

    # Store retrieved data in variables
    channel_ids = [row[0] for row in purchased_channels]
    channel_titles = [row[1] for row in purchased_channels]
    channel_prices = [row[2] for row in purchased_channels]
    print(channel_ids, channel_titles, channel_prices)

    #return channel_ids, channel_titles, channel_prices'''
