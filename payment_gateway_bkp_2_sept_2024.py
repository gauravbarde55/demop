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

from __main__ import app

# app = Flask(__name__)

PAYTM_MERCHANT_ID = 'BSEIns62317292671135'
PAYTM_MERCHANT_KEY = 'GOv7LYGl4eHVPA_x'

order_id = 'ORDER' + str(int(time.time()))  # Unique order ID


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
    # user_id = session.get('uid')
    # print(user_id)
    # user_id = session['uid']
    if 'uid' in session:
        user_id = session.get('uid')
        print("userid from session")
    else:
        print('No user id')
    # if(user_id!=None):
    #     print("user_id")
    #     print(user_id)
    
    # uidd=os.geteuid()
    # uidd=os.getpid()
    # print (os.geteuid())
    user_name = session.get('username')  # Default to 'Guest' if not in session
    print('user_email........')
    # print(user_id)
    print(user_name)
    # if current_user.is_authenticated:
    # URL:"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=BSEIns62317292671135&orderId=PAYTM_ORDER_582720"

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
    return render_template('pay.html',data=paytmParams,presponse=response, PAYTM_BASE_URL=url,checksumpay=checksum)

@app.route('/paytm_callback', methods=['GET','POST'])
def paytm_callback():
    data = request.form.to_dict()
    print("Response Data:", data)

    checksum = data.pop('signature', None)
    MERCHANT_KEY = 'GOv7LYGl4eHVPA_x'
    # if verify_checksum(data, PAYTM_MERCHANT_KEY, checksum):
    if data['STATUS'] == 'TXN_SUCCESS':
        return 'Payment Successful'
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
