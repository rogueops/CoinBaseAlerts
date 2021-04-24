import smtplib, ssl
import requests
import json
import time
#
# v1.0.1.24 of CBP Alert Script
# Created By: Nicore
#

def api():
    # change DNT to the coin you want to watch
    # exmples are MANA-USDC or REN-USD
    # you can find the pair in the web address on coinbase
    api = "https://api.coinbase.com/v2/prices/DNT-USD/buy/"
    response = requests.get(api)
    data = response.text
    parsed = json.loads(data)
    current = (parsed['data']['amount'])
    return current

def emailLow():
    port = 465
    smtp_server = "smtp.DOMAIN.com"
    sender_email = "EMAIL@DOMAIN.com"
    receiver_email = "TO_ADDRESS"
    password = "PasswordHere"
    current = api()
    message = """
	Subject: Low Price Alert!
            Current price is %s.
     """ % (current)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def emailHigh():
    port = 465
    smtp_server = "smtp.DOMAIN.com"
    sender_email = "EMAIL@DOMAIN.com"
    receiver_email = "TO_ADDRESS"
    password = "PasswordHere"
    current = api()
    message = """
	Subject: High Price Alert!
            Current price is %s.
     """ % (current)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def priceAlert():
	# price alert limits
    target_low = float('0.105')
    target_high = float('0.345')

    while True:
        current = api()
        if current < target_low:
            emailLow()
			# comment or remove prints for crontab
            print("Low Alert Sent")
            print("Limit: ", target_low) 
            print("Current Price: ", current)
            break
        elif current > target_high:
            emailHigh()
			# comment or remove prints for crontab
            print("High Alert Sent")
            print("Limit: ",target_high) 
            print("Current Price: ", current)
            break
        else:
            # Comment or remove sleep for contab usage
            time.sleep(1)
            continue

priceAlert()