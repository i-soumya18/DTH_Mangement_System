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

