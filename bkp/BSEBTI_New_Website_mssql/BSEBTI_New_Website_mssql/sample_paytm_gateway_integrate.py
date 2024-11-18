from flask import Flask, request, render_template_string, redirect
import requests
import hashlib

app = Flask(__name__)

# Paytm credentials
PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
PAYTM_ENVIRONMENT = 'production'  # or 'sandbox'
PAYTM_BASE_URL = 'https://secure.paytm.in/theia/processTransaction' if PAYTM_ENVIRONMENT == 'production' else 'https://securegw-stage.paytm.in/theia/processTransaction'
PAYTM_API_URL = 'https://secure.paytm.in/oltp/HANDLER_INTERNAL/'

@app.route('/')
def index():
    return render_template_string('''
        <form action="/pay" method="post">
            <input type="hidden" name="amount" value="10.00">
            <button type="submit">Pay Now</button>
        </form>
    ''')

@app.route('/pay', methods=['POST'])
def pay():
    amount = request.form['amount']
    order_id = 'ORDER' + str(int(time.time()))  # Unique order ID
    data = {
        'MID': PAYTM_MERCHANT_ID,
        'ORDER_ID': order_id,
        'TXN_AMOUNT': amount,
        'CUST_ID': 'CUSTOMER001',  # Replace with actual customer ID
        'CHANNEL_ID': 'WEB',
        'WEBSITE': 'WEBSTAGING',  # or 'DEFAULT' for production
        'INDUSTRY_TYPE_ID': 'Retail',
        'CALLBACK_URL': 'http://yourdomain.com/callback'
    }

    # Generate checksum
    checksum = generate_checksum(data, PAYTM_MERCHANT_KEY)
    data['CHECKSUMHASH'] = checksum

    return render_template_string('''
        <form action="{{ PAYTM_BASE_URL }}" method="post">
            {% for key, value in data.items() %}
                <input type="hidden" name="{{ key }}" value="{{ value }}">
            {% endfor %}
            <button type="submit">Pay Now</button>
        </form>
    ''', data=data, PAYTM_BASE_URL=PAYTM_BASE_URL)

@app.route('/callback', methods=['POST'])
def callback():
    data = request.form.to_dict()
    checksum = data.pop('CHECKSUMHASH', None)
    
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

def verify_checksum(params, key, checksum):
    # Recalculate checksum
    return generate_checksum(params, key) == checksum

if __name__ == '__main__':
    app.run(debug=True)
