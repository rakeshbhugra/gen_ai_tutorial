import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys

load_dotenv()

sender_email = "rakeshkbhugra@gmail.com"
receiver_email = "rakeshkbhugra@gmail.com"
password = os.getenv("EMAIL_APP_PASSWORD")

if not password:
    print("❌ Error: EMAIL_APP_PASSWORD not found in .env file")
    sys.exit(1)

try:
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test Email from Python"
    
    body = "Hello! This is a test email sent using Python and Gmail SMTP."
    message.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure the connection
    
    server.login(sender_email, password)
    
    server.sendmail(sender_email, receiver_email, message.as_string())
    
    server.quit()
    
    print("✅ Email sent successfully!")
    
except smtplib.SMTPAuthenticationError:
    print("❌ Authentication failed. Check your email and app password.")
except smtplib.SMTPException as e:
    print(f"❌ SMTP error occurred: {e}")
except Exception as e:
    print(f"❌ An error occurred: {e}")

