import smtplib
from email.mime.text import MIMEText


def send_email(subject, message, to_addr):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your-email@example.com'
    msg['To'] = to_addr

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
