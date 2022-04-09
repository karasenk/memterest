import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_message(email, text, title, picturename=None):
    adr_from = os.getenv('FROM')
    password = os.getenv('PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = adr_from
    msg['To'] = email
    msg['Subject'] = title
    msg.attach(MIMEText(text, 'plain'))

    if picturename:
        f = open(picturename, 'rb')
        data = f.read()
        f.close()
        file = MIMEImage(data, _subtype='png')
        file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(picturename))
        msg.attach(file)
    server = smtplib.SMTP_SSL(os.getenv('HOST'), os.getenv('PORT'))
    server.login(adr_from, password)
    server.send_message(msg)
    server.quit()
    return True
