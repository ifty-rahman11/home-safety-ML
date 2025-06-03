import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time
from glob import glob

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "SENDER EMAIL"
EMAIL_PASSWORD = "SENDER EMAIL PASSWORD"  
RECEIVER_EMAIL = "RECEIVER EMAIL"

# Email subject and body
SUBJECT = "Intruder ALERT"
BODY = "An intruder was detected. See attached image for details."

# Directory where intruder images are saved
INTRUDER_DIR = "intruder_images"

# Send interval (seconds) - 30 seconds in this case
SEND_INTERVAL = 30
last_sent_time = 0  # Keeps track of the last sent email time


def send_intruder_alert():
    global last_sent_time
    current_time = time.time()

    # Check if enough time has passed since the last email
    if current_time - last_sent_time < SEND_INTERVAL:
        print("Skipping email; 30 seconds have not passed since the last alert.")
        return

    # Find the latest intruder image
    list_of_files = glob(os.path.join(INTRUDER_DIR, "*.jpg"))
    if not list_of_files:
        print("No intruder images found.")
        return
    latest_file = max(list_of_files, key=os.path.getctime)

    # Compose email
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = SUBJECT
        message.attach(MIMEText(BODY, "plain"))

        # Attach the intruder image
        with open(latest_file, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(latest_file)}")
        message.attach(part)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

        print(f"Intruder alert email sent successfully! Attached: {os.path.basename(latest_file)}")
        last_sent_time = current_time  # Update the last sent time
    except Exception as e:
        print(f"Unable to send email: {e}")


if __name__ == "__main__":
    if not os.path.exists(INTRUDER_DIR):
        print(f"Directory '{INTRUDER_DIR}' does not exist. Creating it.")
        os.makedirs(INTRUDER_DIR)

    send_intruder_alert()
