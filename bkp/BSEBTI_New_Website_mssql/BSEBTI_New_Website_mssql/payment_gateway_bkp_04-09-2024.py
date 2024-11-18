import requests
import json
from flask import Flask, render_template, request, redirect, session, url_for

# from flask_login import current_user
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
# import PaytmChecksum
from paytmchecksum import PaytmChecksum
from Crypto.Cipher import AES

import time
import os

import mysql.connector

import MySQLdb

from __main__ import app

# app = Flask(__name__)

# # Database configuration
# db_config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'database': 'enquiry_db'
# }

# Set a secret key for session management
# app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'enquiry_db'

# Initialize MySQL
mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

##############################

PAYTM_MERCHANT_ID = 'BSEIns62317292671135'
PAYTM_MERCHANT_KEY = 'GOv7LYGl4eHVPA_x'

order_id = 'ORDER' + str(int(time.time()))  # Unique order ID

course_id=[]
#Init user session

# @app.callback(
#     Output('user-div', 'children'),
# #     [Input('user-div', 'id')])
# def cur_user(input1):
#     if current_user.is_authenticated:
#         return 'Current user: '+current_user.username
#     else:
#         return 'User non authenticated' # or 'some fake value', whatever





@app.route('/payment_page', methods=['GET','POST'])
def payment_page():
    return render_template('payment_page.html')
    # return render_template_string('''
    #     <form action="/pay" method="post">
    #         <input type="hidden" name="amount" value="10.00">
    #         <button type="submit">Pay Now</button>
    #     </form>
    # ''')
# @login_required
@app.route('/pay', methods=['GET','POST']) ############## To be call on Proceed to payment Button

def pay():

    
    # user_email = session.get('id')  # Default to 'Guest' if not in session
    # alsess=session.all('*')
    # user_id = session.get('user_id')  # Default to 'Guest' if not in session
    print(session)
    # course_name_id=request.form('course_name_id')
    course_name_id=request.form.to_dict()
    print('course_name_id')
    print(course_name_id)
    # user_id = session.get('uid')
    # print(user_id)
    # user_id = session['uid']
    if 'uid' in session:
        user_id = session.get('uid')
        print("userid from session")

        user_name = session.get('username')  # Default to 'Guest' if not in session
        print('user_email........')
        print(user_id)
        print(user_name)
        # if current_user.is_authenticated:
        # URL:"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=BSEIns62317292671135&orderId=PAYTM_ORDER_582720"

        #################################################### Payment Gateway Starts ########################################
        amounts=request.form['amount']
        print('amount......')
        print(amounts)
        paytmParams = dict()

        paytmParams["body"] = {
        "requestType" : "Payment",
        "mid" : PAYTM_MERCHANT_ID,
        "websiteName" : "YOUR_WEBSITE_NAME",
        "orderId" : order_id,
        #  "orderId" : "PAYTM_ORDER_582720",
        # "callbackUrl" : "http://127.0.0.1:5000/paytm_callback",
        "callbackUrl" : "http://localhost:5000/paytm_callback",
        "txnAmount" : {
        "value" : "1.00",
        # "value" : amounts,
        "currency" : "INR",
        },
        "userInfo" : {
        "custId" : "CUST_001",
        },
        }

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

        paytmParams["head"] = {
        "signature" : checksum
        }

        post_data = json.dumps(paytmParams)

        # for Staging
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid="+PAYTM_MERCHANT_ID+"&orderId="+order_id

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        print(response)
        course_id.clear()
        course_id.append(course_name_id)
        print('course_id')
        print(course_id)
        return render_template('pay.html',data=paytmParams,presponse=response, PAYTM_BASE_URL=url,checksumpay=checksum,course_name_id=course_name_id)

    else:
        print('Please Login')
        return render_template('login.html')
    # if(user_id!=None):
    #     print("user_id")
    #     print(user_id)
    
    # uidd=os.geteuid()
    # uidd=os.getpid()
    # print (os.geteuid())
    

@app.route('/paytm_callback', methods=['GET','POST'])
def paytm_callback():

    user_id = session.get('uid')
    data = request.form.to_dict()
    print("Response Data:", data)
    if course_id:
        coursenid=course_id[0]['course_name_id']
        print('coursenid')
        print(coursenid)
    else:
        # return "Refresh Page to Home"
        coursenid='1'


    cursor = mysql.cursor()
    # cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
    cursor.execute('SELECT * FROM course_names WHERE id= %s',(coursenid[0][0]))
    course_name_display = cursor.fetchone()

    print("course_name_display")
    print(course_name_display)
    course_type_id_str=str(course_name_display[2])
    course_type_name_str=str(course_name_display[1])
    course_type_name_id_str=str(course_name_display[0])
    print('Course Type ID: ',course_type_id_str)
    print("Course Name: ",course_type_name_str)
    print('course Name ID: ',course_type_name_id_str)
    # cursor.close()

    try:
        cursor.execute('INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES (%s, %s, %s, %s)', (user_id,course_type_id_str, course_type_name_str,course_type_name_id_str))
        mysql.commit()
        return "Success"

    except MySQLdb.IntegrityError:
            # Handle the error for duplicate username
            mysql.rollback()  # Rollback the transaction
            return 'Username already exists. Please choose a different username.'
    finally:
        cursor.close()
    # connection = mysql.connector.connect(**db_config)
    # cursor = connection.cursor()
    # # query = 'SELECT * FROM course_names WHERE id='+coursenid[0][0]
    # query = 'SELECT * FROM course_names WHERE id='+coursenid
    # cursor.execute(query)
    # fet_course_name = cursor.fetchall()
    # print('fet_course_name')
    # print(fet_course_name)
    # user_id_str=str(user_id)
    # course_type_id_str=str(fet_course_name[0][2])
    # course_type_name_str=str(fet_course_name[0][1])
    # course_type_name_id_str=str(fet_course_name[0][0])

    # print(fet_course_name[0][0])
    # [(1, 'BMS in Capital Markets (MU)', 1, 2000)]
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type,enrollment_course_name,enrollment_course_name_id) VALUES ('"+user_id+"','"+fet_course_name[0][2]+"','"+fet_course_name[0][1]+"','"+fet_course_name[0][0]+"')"
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES ("+user_id+","+fet_course_name[0][2]+",'"+fet_course_name[0][1]+"',"+fet_course_name[0][0]+")"
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES ("+user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str+")"
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES (%s, %s, %s, %s)" # ("+user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str+")"
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES (%s, %s, %s, %s)"
    # cursor.execute(query1,(user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str))
    # print("1 record inserted, ID:", mycursor.lastrowid)
    # q1val=(user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str)
    # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES (%s, %s, %s, %s,)", (user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str)
    # cursor.execute(query1,(user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str), multi=True)
    # cursor.execute(query1,q1val)
    connection.commit()


    checksum = data.pop('signature', None)
    MERCHANT_KEY = 'GOv7LYGl4eHVPA_x'
    # if verify_checksum(data, PAYTM_MERCHANT_KEY, checksum):
    if data['STATUS'] == 'TXN_SUCCESS':
        print('data return')
        print(data)
        print()
        # return 'Payment Successful'
        payment_errors = []
        payment_errors.append('Payment Successful!')
        success_response_data=data

        #########################################################################
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        # query = 'SELECT * FROM course_names WHERE id='+coursenid[0][0]
        query = 'SELECT * FROM course_names WHERE id='+coursenid
        cursor.execute(query)
        fet_course_name = cursor.fetchall()
        print('fet_course_name')
        print(fet_course_name)

        user_id_str=str(user_id)
        course_type_id_str=str(fet_course_name[0][2])
        course_type_name_str=str(fet_course_name[0][1])
        course_type_name_id_str=str(fet_course_name[0][0])

        # print(fet_course_name[0][0])
        # [(1, 'BMS in Capital Markets (MU)', 1, 2000)]
        # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type,enrollment_course_name,enrollment_course_name_id) VALUES ('"+user_id+"','"+fet_course_name[0][2]+"','"+fet_course_name[0][1]+"','"+fet_course_name[0][0]+"')"
        # query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES ("+user_id+","+fet_course_name[0][2]+",'"+fet_course_name[0][1]+"',"+fet_course_name[0][0]+")"
        query1="INSERT INTO enrollments (enrollment_fk_user_id,enrollment_course_type_id,enrollment_course_name,enrollment_course_name_id) VALUES (%s, %s, %s, %s)", (user_id_str,course_type_id_str,course_type_name_str,course_type_name_id_str)
        cursor.execute(query1)
        connection.commit()
        # cursor.close()
        #########################################################################
        return render_template('success_transaction.html',txn_status_data=success_response_data,payment_errors=payment_errors,course_name_id=coursenid)
    else:
        return 'Payment Failed'
    # else:
    #     return 'Checksum Mismatch'
    
def verify_checksum(params, key, checksum):
    print('in verify checksum....')
    generated_checksum =PaytmChecksum.generateSignature(json.dumps(params), key)
    # generated_checksum = generate_checksum(params, key)
    return generated_checksum == checksum

# if __name__ == '__main__':
#     app.run(debug=True)
