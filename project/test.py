import smtplib

from email.mime.text import MIMEText

msg = MIMEText('Testing some Mailgun awesomness')
msg['Subject'] = "Hello"
msg['From']    = ""
msg['To']      = ""

s = smtplib.SMTP('smtp.mailgun.org', 587)

s.login('', '')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
