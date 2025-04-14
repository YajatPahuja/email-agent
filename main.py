import smtplib
import pandas as pd
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv() 

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CSV_FILE = 'data/emails.csv'
BODY_FILE = 'data/email_body.txt'
RESUME_PATH = 'data/resume.pdf'

# --- READ EMAIL CONTENT ---
with open(BODY_FILE, 'r') as file:
    lines = file.readlines()
subject = lines[0].replace("Subject: ", "").strip()
body_template = ''.join(lines[2:])  # Skip subject and empty line

contacts = pd.read_csv(CSV_FILE, header=None, names=['Email'])

for _, row in contacts.iterrows():
    recipient_email = row['Email'].strip()

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg.set_content(body_template)

    with open(RESUME_PATH, 'rb') as f:
        file_data = f.read()
        file_name = Path(RESUME_PATH).name
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send to {recipient_email}: {e}")