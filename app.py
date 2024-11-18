# # Create Virtual Environment
# py -m venv venv
# venv\Scripts\activate

# python -m ensurepip --upgrade

# # Install Libraries
# pip install requests
# pip install Flask
# pip install paytmchecksum
# pip install crypto
# pip install mysql-connector
# pip install mysqlclient

# py -m pip install --upgrade pip

# python -m pip install pycryptodome

#### Crypto Issue
# pip uninstall crypto
# pip uninstall pycryptodome
# pip install pycryptodome



from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
# import mysql.connector  /// For Mysql
import os
import random
import time
import requests
# from flask_mysqldb import MySQL


import pymssql
from config import Config

app = Flask(__name__,static_url_path='/static', static_folder='static')
# mysql = MySQL(app) #### Another Method of Calling mysql
# import declared routes

import page_routes
import user_registration
import payment_gateway


############################
from flask_talisman import Talisman

# Define your CSP directives
# csp = {
#     'default-src': ["'self'"],
#     'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://securegw-stage.paytm.in"],
#     # Add other directives as needed
# }

# csp = {
#     'default-src': ["*"],  # Allow all origins for testing
#     'script-src': ["*"],   # Allow all scripts for testing
# }

csp = {
    'default-src': ["'self'"],
    'script-src': [
        "'self'",
        "'unsafe-inline'",
        "'unsafe-eval'",
        "https://securegw-stage.paytm.in"
    ],
    # Add other directives as needed, like style-src, img-src, etc.
}

# Initialize Talisman with the CSP settings
Talisman(app, content_security_policy=csp)
############################

# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

BROCHURE_DIRECTORY ='static'
# BROCHURE_FILENAME='BMS-in-Capital-Markets.pdf'
BROCHURE_FILENAME=''

app.config.from_object(Config)

def get_db_connection():
    conn = pymssql.connect(
        server=app.config['SQL_SERVER'],
        user=app.config['SQL_USERNAME'],
        password=app.config['SQL_PASSWORD'],
        database=app.config['SQL_DATABASE']
    )
    return conn


# Database configuration
# db_config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'database': 'enquiry_db'
# }

# Temporary storage for OTPs
otp_store = {}

# @app.after_request
# def add_security_headers(response):
#     response.headers['Content-Security-Policy'] = "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
#     return response

# @app.after_request
# def add_security_headers(response):
#     response.headers['Content-Security-Policy'] = (
#         "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://securegw-stage.paytm.in; "
#         "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
#     )
#     return response


@app.route('/', methods=['GET', 'POST'])
# @app.route('/bms_in_capital_markets', methods=['GET', 'POST'])
def index():
    # nonce = uuid.uuid4().hex  # Generate a unique nonce
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()
    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    # query = 'SELECT * FROM btitable'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # rows = cursor.fetchall()
    for row in all_cities:
        print(row)
    print('all_cities')
    print(all_cities)
    print(row)
    # cursor.close()
    cursor1 = connection.cursor()
    # cursor1 = connection.cursor(buffered=True)
    query1 ="SELECT * FROM qualifications"
    # query1 = 'SELECT * FROM btitable'
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    # return qualifcations,200
    # return render_template('index.html', all_cities=all_cities, qualifications=qualifications)
    # response = make_response(render_template('index.html', all_cities=row, qualifications=qualifications))
    # response.headers['Content-Security-Policy'] = "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
    # return response

    return render_template('index.html', all_cities=row, qualifications=qualifications)
    # return render_template('index.html', all_cities=row, qualifications=qualifications,nonce=nonce)

    # return render_template('form.html', all_cities=all_cities, qualifications=qualifications)
    # return render_template('index.html')


@app.route('/form')

def form():
    return render_template('form.html')


@app.route('/qualifications', methods=['GET'])

def get_qualifications():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    # cur = mysql.connection.cursor()
    cur = connection.cursor()
    cur.execute("SELECT * FROM qualifications")
    qualifcation = [dict(qualid=row[0],qualname=row[1]) for row in cur.fetchall()]
    cur.close()
    return jsonify(qualifcation)


@app.route('/countries', methods=['GET'])

def get_countries():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    # cur = mysql.connection.cursor()
    cur = connection.cursor()
    cur.execute("SELECT name FROM countries")
    countries = [dict(name=row[0]) for row in cur.fetchall()]
    cur.close()
    return jsonify(countries)

@app.route('/states', methods=['GET'])

def get_states():
    country = request.args.get('country')
    # cur = mysql.connection.cursor()
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cur = connection.cursor()
    # Get country_id
    cur.execute("SELECT id FROM countries WHERE name = %s", [country])
    country_id = cur.fetchone()
    if country_id:
        country_id = country_id[0]
        # Get states for the country
        cur.execute("SELECT name FROM states WHERE country_id = %s", [country_id])
        states = [state[0] for state in cur.fetchall()]
    else:
        states = []
    cur.close()
    return jsonify(states)

@app.route('/course_types', methods=['GET'])

def get_course_types():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    # cur = mysql.connection.cursor()
    cur = connection.cursor()
    cur.execute("SELECT id,course_name FROM course_type")
    course_types = [dict(coursetype_id=row[0],coursetype_name=row[1]) for row in cur.fetchall()]
    cur.close()
    return jsonify(course_types)

@app.route('/course_names', methods=['GET'])

def get_course_names():
    courses_types = request.args.get('courses_types') ######## Textbox id
    # print('courses_types')
    # print(courses_types)
    # cur = mysql.connection.cursor()
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cur = connection.cursor()
    # Get country_id
    cur.execute("SELECT id FROM course_type WHERE id = %s", [courses_types]) #### 
    course_type_id = cur.fetchone()
    if course_type_id:
        course_type_id = course_type_id[0]
        # Get states for the country
        cur.execute("SELECT id,course_name FROM course_names WHERE fk_course_type_id = %s", [course_type_id])
        # states = [course_name[0] for course_name in cur.fetchall()]
        states = [dict(course_name_id=courses_name[0],course_name=courses_name[1]) for courses_name in cur.fetchall()]
    else:
        states = []
    cur.close()
    return jsonify(states)


@app.route('/send_otp', methods=['POST'])

def send_otp():
    data = request.get_json()
    mobile = data['mobile']
    # Generate and store OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    otp_store[mobile] = (otp, time.time())
    timeval=5
    # # Generate and store OTP
    # otp = random.randint(100000, 999999)
    # otp_store[mobile] = (otp, time.time())
    # Here, you should send OTP to the user's mobile number using an SMS service API

    #############################################################################
    url = "http://www.alots.in/sms-panel/api/http/index.php"

    params = {
        'username': 'BSEINDIAOTP',
        'apikey': '04953-629DB',
        'apirequest': 'Text',
        'sender': 'Bsebti',
        # 'mobile': '917208488321',
        'mobile': mobile,
        # 'message': 'Your OTP for Registration into BSE Institute Ltd. is {#var#}. It will expire in {#var#} minutes.',
        # 'message': 'Your OTP for Registration into BSE Institute Ltd. is '+ str(otp) +'. It will expire in '+str(timeval)+' minutes.',
        'message': 'Your OTP for Registration into BSE Institute Ltd. is '+ str(otp) +'. It will expire in '+ str(timeval) +' minutes.',
        'route': 'OTP',
        # 'TemplateID': '1207162512861161028',
        'TemplateID': '1207172266944540768',
        
        'format': 'JSON'
    }

    ################################### Comment this section Start
    print('otp is -- ')
    print(otp)
    ################################### Comment this section End

    ################################### UnComment this section Start
    # Send the request
    response = requests.get(url, params=params)

    # # Check the response
    if response.status_code == 200:
        print("SMS sent successfully.")
        print("Response:", response.json())
        # return 'response sms'
        # return otp_storage
    else:
        print("Failed to send SMS.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    ################################### UnComment this section End
    #############################################################################

    # For demonstration purposes, we'll just print the OTP
    print(f"Generated OTP for {mobile}: {otp}")
    return jsonify({'success': True})


@app.route('/verify_otp', methods=['POST'])

def verify_otp():
    data = request.get_json()
    otp = data['otp']
    mobile = data['mobile']
    print('otp')
    print(otp)
    stored_otp, timestamp = otp_store.get(mobile, (None, None))
    # OTP validity check (e.g., 5 minutes)
    # if stored_otp and stored_otp == int(otp) and time.time() - timestamp < 300:
    if stored_otp and stored_otp == otp and time.time() - timestamp < 300:
        del otp_store[mobile]  # Clear OTP after verification
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/submit', methods=['POST'])

def submit():

    brochure_name=request.form['brochure_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    mobile = request.form['mobile']
    city = request.form['all_cities']
    message = request.form['message']

    # course_type=request.form['courses_types']

    qualifications=request.form['qualification']
    course_type=request.form['courses_types']
    course_name=request.form['courses_names']
    # Connect to the database
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    # Insert data into the database
    # query = 'INSERT INTO enquiries (name, email, mobile, message) VALUES (%s, %s, %s, %s)'
    query = 'INSERT INTO enquiries (first_name, last_name, email, mobile, city, message,fk_qualification_id,fk_course_type_id,fk_course_name_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (first_name, last_name, email, mobile, city, message,qualifications,course_type,course_name))
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    global BROCHURE_FILENAME1

    global BROCHURE_DIRECTORY1
    BROCHURE_FILENAME1=brochure_name+'.pdf'

    if(course_type=='1'):
        print('1 of Under Graduate Called')
        BROCHURE_DIRECTORY1='static/brochures/ug'
    elif(course_type=='2'):
        print('2 of POST Graduate Called')
        BROCHURE_DIRECTORY1='static/brochures/pg'
    elif(course_type=='3'):
        print('3 of Professional Studies Called')
        BROCHURE_DIRECTORY1='static/brochures/ps'
    elif(course_type=='4'):
        print('4 of Vocational Courses Called')
        BROCHURE_DIRECTORY1='static/brochures/vc'
    elif(course_type=='5'):
        print('5 of MicroX Called')
        BROCHURE_DIRECTORY1='static/brochures/microx'
    elif(course_type=='6'):
        print('6 of ProfX Called')
        BROCHURE_DIRECTORY1='static/brochures/profx'
    print('BROCHURE_FILENAME')
    print(BROCHURE_FILENAME1)
    if(brochure_name==''):
        return redirect(url_for('no_brochure'))
    else:
        return redirect(url_for('download_brochure'))

    # return redirect(url_for('download_brochure'))
    # return redirect(url_for('download_brochure'))
@app.route('/no_brochure')

def no_brochure():
    return "No Brochure Available for This Course"

@app.route('/download_brochure')

def download_brochure():
    brochure_path = os.path.join('static', 'brochure.pdf')
    print('Download Brochure Called')
    print(BROCHURE_FILENAME1)
    print(BROCHURE_DIRECTORY1)
    # Brochure_filename=BROCHURE_FILENAME1
    # print(Brochure_filename)
    # Check whether a path pointing to a file
    # isFile = os.path.isfile(BROCHURE_FILENAME1)
    # print(isFile)
    # if()
    return send_from_directory(directory=BROCHURE_DIRECTORY1, path=BROCHURE_FILENAME1, as_attachment=True)
    # return send_from_directory(directory='static', path=BROCHURE_FILENAME1, as_attachment=True)
    # return send_from_directory(directory='static', path='brochure.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

