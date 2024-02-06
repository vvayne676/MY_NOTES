```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def send_email(sender_email, receiver_email,cc_email, password, subject, body, attachment_path):
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = cc_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open the file to be sent
    with open(attachment_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)

    # Connect to SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password,initial_response_ok=True)
        server.sendmail(sender_email, [receiver_email] + cc_email.split(','), message.as_string())

```

```python
shoot_email.send_email(
        sender_email="wuwenlong@xcloudgame.com",
        receiver_email="wuwenlong@xcloudgame.com",
        cc_email="wuwenlong@xcloudgame.com",
        password="ikvo vqhq fyao nwvl",
        subject="Today's statement",
        body="empty body",
        attachment_path=f'{ymd}.csv')
```
Ref: https://mailtrap.io/blog/python-send-email-gmail/ 

pip install urllib3==1.25.11 

password is generated from Google dashboard 2 factors verification part.