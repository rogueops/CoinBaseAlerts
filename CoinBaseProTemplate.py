import smtplib, ssl, time
import json, requests, cbpro
from itertools import islice
#
# v2.1.6 of CBP Alert Script
# Created By: Nicore
#

def api():
    key = "ENTER_CB_KEY"
    secret = "ENTER_CB_SECRET"
    password = "ENTER_CB_PASSWORD"
    auth_client = cbpro.AuthenticatedClient(key, secret, password)
    # change below pair to coin wanted, most are COIN-USD or COIN-USDC
    data = auth_client.get_product_ticker('BTC-USD')
    current = (data['price'])
    return float(current)

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
     """ %(current)

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
     """ %(current)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def priceAlert():
	# price alert limits
    target_low = float('4.9')
    target_high = float('5.2')

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
            # Uncomment prints to have heartbeat messages
            #print("No price alert emails sent....\n")
            #print("Sleeping for 5 seconds...\n")
            # Comment or remove sleep for contab usage
            time.sleep(5)
            # Replace continue with break for crontab usage
            continue

priceAlert()