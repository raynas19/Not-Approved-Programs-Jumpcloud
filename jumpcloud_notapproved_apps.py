import requests
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta


# Email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'X’
EMAIL_PASSWORD = 'X'
RECIPIENT_EMAIL = 'X'

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
def send_email_notification(application_name, system_id):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECIPIENT_EMAIL_ADDRESS
    message["Subject"] = "New Not Approved Application Installed: " + application_name
    body = 'Not an approved application: ' + application_name + '\n\n'+ 'Publisher: ' + program_publisher + '\n\n' + 'System ID: ' + system_id + '\n\n' + 'Install Date: ' + program_install_date + '\n\n ' + 'Install Source: ' + program_install_source + '\n'
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL_ADDRESS, message.as_string())


# Loop thought Jumcploud API response
for log in jc_data:
    app_name = log['application']['name']
    program_publisher = log['application']['publisher']
    program_install_date = log['application']['install_date']
    program_install_source = log['application']['install_source']
    system_id = log['application']['system_id']

    if app_name not in approved_apps:
        print("Unapproved application installed:", app_name)
        send_email_notification(application_name, system_id)
    else:
        print("Approved application installed:", app_name)
