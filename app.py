from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data for demonstration (Replace with actual database implementation)
admins = [{'username': 'admin', 'password': 'admin123'}]
customers = [{'username': 'customer', 'password': 'customer123'}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admins.append({'username': username, 'password': password})
        return redirect(url_for('admin_signin'))
    return render_template('admin_signup.html')

@app.route('/admin/signin', methods=['GET', 'POST'])
def admin_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for admin in admins:
            if admin['username'] == username and admin['password'] == password:
                return "Admin signin successful"
        return "Invalid credentials"
    return render_template('admin_signin.html')

@app.route('/customer/signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customers.append({'username': username, 'password': password})
        return redirect(url_for('customer_signin'))
    return render_template('customer_signup.html')

@app.route('/customer/signin', methods=['GET', 'POST'])
def customer_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for customer in customers:
            if customer['username'] == username and customer['password'] == password:
                return "Customer signin successful"
        return "Invalid credentials"
    return render_template('customer_signin.html')

if __name__ == '__main__':
    app.run(debug=True)
