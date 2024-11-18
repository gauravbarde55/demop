from flask import Flask, request, render_template_string, redirect, render_template
import requests
import hashlib

import time

from __main__ import app


# Paytm credentials
# PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
# PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
PAYTM_MERCHANT_ID = 'BSEIns00118007523920'
PAYTM_MERCHANT_KEY = 'DFB74WQ2v7@na%Vj'
PAYTM_ENVIRONMENT = 'sandbox'  # or 'sandbox''production'
PAYTM_BASE_URL = 'https://secure.paytm.in/theia/processTransaction' if PAYTM_ENVIRONMENT == 'production' else 'https://securegw-stage.paytm.in/theia/processTransaction'
PAYTM_API_URL = 'https://secure.paytm.in/oltp/HANDLER_INTERNAL/'

# @app.route('/')
# def index():
@app.route('/payment_page', methods=['GET','POST'])
def payment_page():
    return render_template('payment_page.html')
    # return render_template_string('''
    #     <form action="/pay" method="post">
    #         <input type="hidden" name="amount" value="10.00">
    #         <button type="submit">Pay Now</button>
    #     </form>
    # ''')

@app.route('/pay', methods=['GET','POST']) ############## To be call on Proceed to payment Button
def pay():
    amount = request.form['amount']
    order_id = 'ORDER' + str(int(time.time()))  # Unique order ID
    # data = {
    #     'MID': PAYTM_MERCHANT_ID,
    #     'ORDER_ID': order_id,
    #     'TXN_AMOUNT': amount,
    #     'CUST_ID': 'CUSTOMER001',  # Replace with actual customer ID
    #     'CHANNEL_ID': 'WEB',
    #     'WEBSITE': 'WEBSTAGING', #'WEBSTAGING',  # or 'DEFAULT' for production
    #     'INDUSTRY_TYPE_ID': 'Retail',#'PrivateEducation', # 'Retail',
    #     # 'CALLBACK_URL': 'http://yourdomain.com/callback'
    #     'CALLBACK_URL': 'http://127.0.0.1:5000/callback'
    # }

    data = dict()

    data["body"] = {
    "requestType" : "Payment",
    "mid" : "BSEIns00118007523920",
    # "websiteName" : "YOUR_WEBSITE_NAME",
    "websiteName" : "WEBSTAGING",
    # "websiteName" : "DEFAULT",
    "orderId" : order_id,
    # "callbackUrl" : 'http://localhost:5000/paytm/response',
    "callbackUrl" : 'http://127.0.0.1:5000/callback',
    "txnAmount" : {
    "value" : "1.00",
    "currency" : "INR",
    },
    "userInfo": {
    "custId": "CUST_001",
    },
    }

    # Generate checksum
    checksum = generate_checksum(data, PAYTM_MERCHANT_KEY)
    # print('checkssss')
    # print(checksum)
    # print('datassss')
    # print(data)
    data['CHECKSUMHASH'] = checksum
    # print('data[CHECKSUMHASH]')
    # print(data['CHECKSUMHASH'])

    print(data)

    return render_template('pay.html',data=data, PAYTM_BASE_URL=PAYTM_BASE_URL,checksumpay=checksum)
    # return render_template_string('''
    #     <form action="{{ PAYTM_BASE_URL }}" method="post">
    #         {% for key, value in data.items() %}
    #             <input type="hidden" name="{{ key }}" value="{{ value }}">
    #         {% endfor %}
    #         <button type="submit">Pay Now</button>
    #     </form>
    # ''', data=data, PAYTM_BASE_URL=PAYTM_BASE_URL)

@app.route('/callback', methods=['GET','POST'])
def callback():
    # data1=request.form['CHECKSUMHASH']
    print('data1')
    # print(data1)
    data = request.form.to_dict()
    # cpa=checksumpay
    print('calldata')
    print(data)
    checksum = data.pop('CHECKSUMHASH', None)
    print('checksum')
    print(checksum)
    if checksum is None:
        print("Checksum not received in callback.")
        return "Payment Failed"

    if verify_checksum(data, PAYTM_MERCHANT_KEY, checksum):
        # Payment successful, handle success
        return "Payment Successful"
    else:
        # Payment failed, handle error
        return "Payment Failed"

def generate_checksum(params, key):
    # Create a sorted list of params and encode to UTF-8
    params_str = '&'.join(f'{k}={v}' for k, v in sorted(params.items()))
    # Add the key to the end
    params_str += f'&{key}'
    
    # Create checksum hash
    return hashlib.sha256(params_str.encode('utf-8')).hexdigest()

# def verify_checksum(params, key, checksum):
#     # Recalculate checksum
#     return generate_checksum(params, key) == checksum

def verify_checksum(params, key, checksum):
    print("Received Checksum:", checksum)
    # print("Is Checksum Valid:", valid)
    # Generate checksum from parameters
    generated_checksum = generate_checksum(params, key)
    # Compare with received checksum
    return generated_checksum == checksum
