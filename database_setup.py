import mysql.connector

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="soumya",
        database="dth_data"
    )


# design the dth_data.cart table
def create_cart_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS cart (email VARCHAR(255), channel_id VARCHAR(255), channel_title VARCHAR(255))"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


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

# Function to add channel to the cart
def add_channel(email, channel_data):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO cart (email, channel_id, channel_title) VALUES (%s, %s, %s)"
    cursor.execute(query, (email, channel_data['id'], channel_data['title']))
    connection.commit()
    cursor.close()
    connection.close()


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




