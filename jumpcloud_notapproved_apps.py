import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta


# Email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'X’
EMAIL_PASSWORD = 'X'
RECIPIENT_EMAIL_ADDRESS = 'X'

# API Endpoint
url = "https://api.jumpcloud.com/insights/directory/v1/events"

#Whitelist
approved_apps = ['Google', 'Microsoft Word’']

# Number of minutes to look back in JumpCloud logs
LOOKBACK_MINUTES = 60

# Get the current time and the time to start looking back in the JumpCloud logs
current_time = datetime.utcnow()
lookback_time = current_time - timedelta(minutes=LOOKBACK_MINUTES)

# API REQUEST
payload = {
    "service": ["software"],
    "start_time": lookback_time.isoformat() + 'Z',
    "field": "application",
}
headers = {
    "accept": "application/json",
    "x-api-key": "X",
    "content-type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)


# Parse Jumpcloud API response
jc_data = response.json()

# Email Notification
def send_email_notification(app_name):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECIPIENT_EMAIL_ADDRESS
    message["Subject"] = "New Not Approved Application Installed: " + app_name + ' on ' + device_name
    body = 'Not an approved application: ' + '\n\n'+ app_name + '\n\n'+ 'Device Name: ' + device_name + '\n\n'+ 'Publisher: ' + program_publisher + '\n\n' + 'System ID: ' + system_id + '\n\n' + 'Install Date: ' + program_install_date + '\n\n ' + 'Install Source: ' + program_install_source + '\n'
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL_ADDRESS, message.as_string())


# Loop thought Jumcploud API response
for log in jc_data:
    event_type = log['event_type']
    app_name = log['application']['name']
    device_name = log['system']['hostname']
    program_publisher = log['application']['publisher']
    program_install_date = log['timestamp']
    program_install_source = log['application']['path']
    system_id = log['id']

    if event_type == 'software_add' and app_name not in approved_apps:
        print("Unapproved application installed:", app_name, system_id)
        send_email_notification(app_name)
    #else:
        #print("Approved application installed:", app_name)
