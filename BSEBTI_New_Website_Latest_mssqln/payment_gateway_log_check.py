@app.route('/callback', methods=['POST'])
def callback():
    data = request.form.to_dict()
    checksum = data.pop('CHECKSUMHASH', None)
    
    print("Received callback data:", data)  # Log received data
    print("Received checksum:", checksum)  # Log received checksum

    if verify_checksum(data, PAYTM_MERCHANT_KEY, checksum):
        print("Checksum verification successful")
        # Payment successful, handle success
        return "Payment Successful"
    else:
        print("Checksum verification failed")
        # Payment failed, handle error
        return "Payment Failed"
