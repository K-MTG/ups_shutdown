import smtplib
import requests
import time
from nut2 import PyNUTClient
from subprocess import call

CHECK_INTERVAL = 60  # Seconds - how often to check UPS status
UPS_SHUTDOWN_THRES = 8  # percentage on when to shutdown hub

def shutdown_hubitat():
    ip = '10.0.1.20'  # Hubitat IP Address
    login_data = {  # Hubitat Login Credentials
        'username': 'admin',
        'password': 'mypassword'
    }

    with requests.Session() as s:
        try:
            s.get('http://%s/login' % (ip), timeout=5)
            s.post('http://%s/login' % (ip), data=login_data, timeout=5)
            s.post('http://%s/hub/shutdown' % (ip), timeout=5)
            print("Shutdown Command Sent")
        except:
            print("Shutdown Failed")


def send_email(subject):
    # GMAIL Login
    user = 'myemail@gmail.com'
    pwd = 'mypassword'
    recipient = 'myrecepient@icloud.com'

    body = subject
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except Exception as e:
        print ("failed to send mail")
        print(e)


opt_track = {
    'on_battery_email_sent': False,
    'shutdown_email_sent': False
}

print("Running Script")

while True:
    status = {}
    try:
        client = PyNUTClient()
        status = client.list_vars("ups")
    except:
        pass

    if 'ups.status' not in status or 'battery.charge' not in status:
        print("Can't Reach UPS")
        time.sleep(10)
        continue


    if opt_track['on_battery_email_sent'] is False and status['ups.status'] != "OL":
        print("Power Outage")
        opt_track['on_battery_email_sent'] = True
        send_email('House on UPS Power')

    elif opt_track['on_battery_email_sent'] is True and status['ups.status'] == "OL":
        print("Power Restored")
        opt_track['on_battery_email_sent'] = False
        opt_track['shutdown_email_sent'] = False
        send_email('House Power Restored')

    if opt_track['shutdown_email_sent'] is False and int(status['battery.charge']) <= UPS_SHUTDOWN_THRES and status[
        'ups.status'] != "OL":
        print("Shutting Down")
        opt_track['on_battery_email_sent'] = True
        opt_track['shutdown_email_sent'] = True
        send_email('House - Shutting Down Pi & Hubitat')
        shutdown_hubitat()
        time.sleep(3)
        call("sudo shutdown -h now", shell=True) # Shutdown Raspberry Pi

    time.sleep(CHECK_INTERVAL)
