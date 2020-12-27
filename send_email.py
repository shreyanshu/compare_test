### email modules ###
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from smtplib import SMTPException

def send_an_email():
    toaddr = ['slodha@alumni.deerwalk.edu.np', 'shreyansh.lodha21@gmail.com']
    me = 'dectest123@outlook.com'
    subject = "Result"
    password = 'test!@#123'
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ','.join(toaddr)
    msg.preamble = "test "

    msg.attach(MIMEText('Test test', 'plain'))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("info.xlsx", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="info.xlsx"')
    msg.attach(part)

    try:
       s = smtplib.SMTP('smtp.office365.com', 587)
       s.ehlo()
       s.starttls()
       s.ehlo()
       s.login(user = me, password=password)
       s.sendmail(me, toaddr, msg.as_string())
       s.quit()
    except SMTPException as error:
          print (error.args)

send_an_email()