import yagmail
TO = 'lodahsreyansh12@gmail.com'
SUBJECT = 'test email'
TEXT = 'details go here'

yag = yagmail.SMTP('dectest123@outlook.com', 'test!@#123', host='smtp.office365.com', port=587, smtp_starttls=True,
                   smtp_ssl=False)
yag.send(TO, SUBJECT, TEXT)