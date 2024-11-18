import hashlib
import time
from flask import Flask, request, render_template_string, render_template

import json
import hashlib
import hmac

from paytmchecksum import PaytmChecksum
from Crypto.Cipher import AES

app = Flask(__name__)



PAYTM_MERCHANT_ID = 'BSEIns00118007523920'
PAYTM_MERCHANT_KEY = 'DFB74WQ2v7@na%Vj'
# PAYTM_BASE_URL = 'https://securegw-stage.paytm.in/theia/processTransaction'
PAYTM_BASE_URL = 'https://securegw-stage.paytm.in/theia/processTransaction?mid=' + PAYTM_MERCHANT_ID + '&orderId='

# PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
# PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'

@app.route('/')
def index():
    return 'Paytm Integration Test'

@app.route('/pay_test')
def pay_test():
    return render_template('paytest.html')


def generate_checksum(params, key):
    params_str = '&'.join(f'{k}={v}' for k, v in sorted(params.items()))
    params_str += f'&{key}'
    return hashlib.sha256(params_str.encode('utf-8')).hexdigest()

@app.route('/pay', methods=['POST'])
def pay():

    MERCHANT_ID = 'BSEIns00118007523920'
    MERCHANT_KEY = 'DFB74WQ2v7@na%Vj'
    amount = request.form['amount']
    # amount1 = request.form['cform']
    print('amount1')
    # print(amount1)
    order_id = 'ORDER' + str(int(time.time()))  # Unique order ID
    # data = {
    #     'MID': PAYTM_MERCHANT_ID,
    #     'ORDER_ID': order_id,
    #     'TXN_AMOUNT': amount,
    #     'CUST_ID': 'CUSTOMER001',
    #     'CHANNEL_ID': 'WEB',
    #     'WEBSITE': 'WEBSTAGING',
    #     'INDUSTRY_TYPE_ID': 'Retail',
    #     'CALLBACK_URL': 'http://localhost:5000/callback'
    # }

    params = {
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

    checksum = PaytmChecksum.generateSignature(json.dumps(params["body"]), MERCHANT_KEY)
    # checksum = generate_checksum(params, PAYTM_MERCHANT_KEY)
    params['CHECKSUMHASH'] = checksum
    PAYTM_BASE_URL1 = PAYTM_BASE_URL + order_id
    print('check base url')
    print(PAYTM_BASE_URL1)

    return render_template('checkmis.html', params=params, PAYTM_BASE_URL=PAYTM_BASE_URL1)
    # return render_template_string('''
    #     <form action="{{ PAYTM_BASE_URL }}" method="post">
    #         {% for key, value in data.items() %}
    #             <input type="hidden" name="{{ key }}" value="{{ value }}">
    #         {% endfor %}
    #         <button type="submit">Pay Now</button>
    #     </form>
    # ''', data=data, PAYTM_BASE_URL=PAYTM_BASE_URL)

# def verify_checksum(params, key, checksum):
def verify_checksum(params, MERCHANT_KEY, checksum):
    generated_checksum =PaytmChecksum.generateSignature(json.dumps(params["body"]), MERCHANT_KEY)
    # generated_checksum = generate_checksum(params, key)
    print("generate_checksum")
    print(generated_checksum)
    return generated_checksum == checksum

@app.route('/callback', methods=['GET','POST'])
def callback():
    print('params')
    # print(params)
    # d = request.form['para']
    # print(d)
    data = request.form.to_dict()
    # checksum = data.pop('CHECKSUMHASH', None)
    checksum= data['TXNAMOUNT']
    
    # Log the received data
    print("Received callback data:", data)
    print("Received Checksum:", checksum)

    if checksum is None:
        return "Checksum Missing"

    if verify_checksum(data, PAYTM_MERCHANT_KEY, checksum):
        return "Payment Successful"
    else:
        return "Payment Failed"

if __name__ == '__main__':
    app.run(debug=True)