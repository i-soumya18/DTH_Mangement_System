from flask import Blueprint, render_template, request, redirect, url_for

customer_blueprint = Blueprint('customer', __name__)

# Dummy data for demonstration (Replace with actual database implementation)
customers = [{'username': 'customer', 'password': 'customer123'}]

@customer_blueprint.route('/customer/signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customers.append({'username': username, 'password': password})
        return redirect(url_for('customer.customer_signin'))
    return render_template('customer_signup.html')

@customer_blueprint.route('/customer/signin', methods=['GET', 'POST'])
def customer_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for customer in customers:
            if customer['username'] == username and customer['password'] == password:
                return "Customer signin successful"
        return "Invalid credentials"
    return render_template('customer_signin.html')
