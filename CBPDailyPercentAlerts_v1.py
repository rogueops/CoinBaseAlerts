import smtplib, ssl, time
import json, requests, cbpro
from itertools import islice

def api():
    key = "ENTER_KEY"
    secret = "ENTER_SECRET"
    password = "ENTER_PASSWORD"
    auth_client = cbpro.AuthenticatedClient(key, secret, password)
    data = auth_client.get_product_ticker('COIN-USDC OR COIN-USD')
    current = (data['price'])
    return current

def emailLow():
    port = 465
    smtp_server = "smtp.MAIL_SERVER.com"
    sender_email = "FROM_ADDRESS"
    receiver_email = "TO_ADDRESS"
    password = "MAIL_ACCOUNT_PASSWORD"
    current = api()
    # edit message between ''' for alert text
    # %s is percent at time of alert
    # %(current) is link to %s for percent
    message = """
	Subject: Daily Percent Down!
            Current daily percent %s.
     """ % (current)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def emailHigh():
    port = 465
    smtp_server = "smtp.MAIL_SERVER.com"
    sender_email = "FROM_ADDRESS"
    receiver_email = "TO_ADDRESS"
    password = "MAIL_ACCOUNT_PASSWORD"
    current = api()
    # edit message between ''' for alert text
    # %s is percent at time of alert
    # %(current) is link to %s for percent
    message = """
    Subject: Daily Percent Up!
            Current daily percent %s.
     """ %(current)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def priceAlert():
	# percent alert limits
    target_low = float('0.098')
    target_high = float('0.15')

    while True:
        current = api()
        if current < target_low:
            emailLow()
			# comment or remove prints for crontab
            # below is text for console
            print("Low Alert Sent")
            print("Limit: ", target_low) 
            print("Current Price: ", current)
            break
        elif current > target_high:
            emailHigh()
			# comment or remove prints for crontab
            # below is text for console
            print("High Alert Sent")
            print("Limit: ",target_high) 
            print("Current Price: ", current)
            break
        else:
            # Uncomment prints to have heartbeat messages
            #print("No alert emails sent....\n")
            #print("Sleeping for 5 seconds...\n")
            # Comment or remove sleep for contab usage
            time.sleep(5)
            # Replace continue with break for crontab usage
            continue

priceAlert()
