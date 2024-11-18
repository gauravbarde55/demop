To retrieve and display cart data that was saved before login, you’ll need to implement a mechanism to manage cart sessions separately from user accounts. This typically involves:

1. **Storing Cart Data Temporarily**: Use a session-based or cookie-based system to track cart items for users who haven’t logged in yet.
2. **Linking Cart Data to User Accounts**: When the user logs in, merge or transfer the temporary cart data to their account.

Here’s a detailed approach to achieve this in Flask:

### 1. **Manage Temporary Cart Data**

Use Flask sessions to store cart data temporarily for users who haven’t logged in. This ensures that users can add items to their cart before logging in or registering.

**`app.py`**

```python
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import MySQLdb
import re
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

# Initialize MySQL
mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    cart = get_cart()

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session['cart'] = cart
    return redirect(url_for('checkout'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        errors = []
        if len(username) < 3 or len(username) > 15:
            errors.append("Username must be between 3 and 15 characters long.")
        if not re.match("^[a-zA-Z0-9_]+$", username):
            errors.append("Username can only contain letters, numbers, and underscores.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if not errors:
            cursor = mysql.cursor()
            cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                errors.append('Username already exists. Please choose a different username.')
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
                mysql.commit()
                user_id = cursor.lastrowid
                cursor.close()

                # Transfer cart data to user
                cart = session.get('cart', {})
                for product_id, qty in cart.items():
                    cursor = mysql.cursor()
                    cursor.execute('INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)', (user_id, product_id, qty))
                    mysql.commit()
                    cursor.close()

                session.pop('cart', None)  # Clear cart after transfer
                session['username'] = username
                return redirect(url_for('checkout'))
        return render_template('register.html', errors=errors)
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[1], password):
            session['username'] = username
            user_id = user[0]

            # Transfer temporary cart to user account
            cart = session.get('cart', {})
            if cart:
                cursor = mysql.cursor()
                for product_id, qty in cart.items():
                    cursor.execute('INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)', (user_id, product_id, qty))
                mysql.commit()
                session.pop('cart', None)  # Clear cart after transfer
                cursor.close()

            return redirect(url_for('checkout'))
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

@app.route('/checkout')
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = get_user_id_by_username(session['username'])
    cursor = mysql.cursor()
    
    try:
        cursor.execute('''
            SELECT p.name, p.price, ci.quantity 
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.user_id = %s
        ''', (user_id,))
        
        cart_items = cursor.fetchall()
        cursor.close()
        
        return render_template('checkout.html', cart_items=cart_items)
    except MySQLdb.Error as e:
        return 'An error occurred while retrieving cart data.'

def get_user_id_by_username(username):
    cursor = mysql.cursor()
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    return user[0] if user else None

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cart', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. **Create the Checkout Template**

**`templates/checkout.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout</title>
</head>
<body>
    <h1>Checkout</h1>
    <p>Welcome, {{ session['username'] }}!</p>
    
    <h2>Your Cart</h2>
    <ul>
        {% for item in cart_items %}
            <li>{{ item[0] }} - ${{ item[1] }} x {{ item[2] }}</li>
        {% endfor %}
    </ul>
    
    <!-- Add checkout form or payment integration here -->
    
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
```

### Summary

1. **Temporary Cart Storage**: Use Flask sessions to manage cart data before login or registration.
2. **Cart Transfer on Login/Registration**: Transfer cart items to the user’s account when they log in or register.
3. **Display Cart Items**: Retrieve and display cart items on the checkout page after login.

### Additional Considerations

- **Cart Expiration**: Consider how long you want to keep cart data in the session.
- **User Experience**: Make sure users are aware of the transfer process from temporary to permanent carts.
- **Security**: Securely handle and validate all user data and session information.

By following these steps, you ensure that users have a smooth transition from a temporary cart to a user-specific cart upon login or registration.