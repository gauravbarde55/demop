from flask import Flask, render_template, redirect, url_for, request, session
# import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
import os

# from __main__ import app

from app import app

import pymssql
from config import Config

# Database configuration
# db_config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'database': 'enquiry_db'
# }

# # Initialize MySQL
# mysql = MySQLdb.connect(
#     host=app.config['MYSQL_HOST'],
#     user=app.config['MYSQL_USER'],
#     password=app.config['MYSQL_PASSWORD'],
#     database=app.config['MYSQL_DB']
# )

# Set a secret key for session management
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'enquiry_db'

# # Initialize MySQL
# mysql = MySQLdb.connect(
#     host=app.config['MYSQL_HOST'],
#     user=app.config['MYSQL_USER'],
#     password=app.config['MYSQL_PASSWORD'],
#     database=app.config['MYSQL_DB']
# )
app.config.from_object(Config)

def get_db_connection():
    conn = pymssql.connect(
        server=app.config['SQL_SERVER'],
        user=app.config['SQL_USERNAME'],
        password=app.config['SQL_PASSWORD'],
        database=app.config['SQL_DATABASE']
    )
    return conn

connection = get_db_connection()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # hashed_password = generate_password_hash(password, method='sha256')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        print("Generated hash:", hashed_password)
        
        # cursor = mysql.cursor()

        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        middle_name=request.form.get('middle_name')
        email_id=request.form.get('email_id')
        contact_no=request.form.get('mobile')

        # Server-side validation
        errors = []
        # if len(username) < 3 or len(username) > 15:
        #     errors.append("Username must be between 3 and 15 characters long.")
        # if not re.match("^[a-zA-Z0-9_]+$", username):
        #     errors.append("Username can only contain letters, numbers, and underscores.")
        # if len(password) < 6:
        #     errors.append("Password must be at least 6 characters long.")

        # Check for unique username
        # if not errors:
        connection = get_db_connection()

        cursor = connection.cursor()
        # cursor = mysql.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            errors.append('Username already exists. Please choose a different username.')

        if errors:
            return render_template('register.html', errors=errors)
        
        # cursor = mysql.cursor()
        cursor = connection.cursor()
        
        try:
            # cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            cursor.execute('INSERT INTO users (username, password, first_name, last_name, middle_name, email_id, contact_no) VALUES (%s, %s,%s, %s,%s, %s, %s)', (username, hashed_password, first_name, last_name, middle_name, email_id, contact_no))
            # mysql.commit()
            connection.commit()
            # cursor.close()
            return redirect(url_for('login'))
        # except MySQLdb.IntegrityError:
        except pymssql.IntegrityError:
            # Handle the error for duplicate username
            connection.rollback()  # Rollback the transaction
            # mysql.rollback()  # Rollback the transaction
            return 'Username already exists. Please choose a different username.'
        finally:
            cursor.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = connection.cursor()
        # cursor = mysql.cursor()
        cursor.execute('SELECT password,id FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        
        print("Stored hash:", user[0])
        print('useid',user[1])
        # print('useid',user[1])
        print("generated hash:", password)
        if user and check_password_hash(user[0], password):
            # print('session data')
            # print(session)
            session['uid']=user[1]
            session['username'] = username
            # print(session['uid'])
            return redirect(url_for('index'))
            # return redirect(url_for('add_to_cart'))
            # return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('uid',None)
    return redirect(url_for('index'))
    # return redirect(url_for('home'))