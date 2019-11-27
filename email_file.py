import smtplib
import argparse
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import configparser
import json

def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1", use_ssl=False, username=None, password=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    print server
    if use_ssl == True:
        smtp = smtplib.SMTP_SSL(server)
    else:
        smtp = smtplib.SMTP(server)

    if username != None and username != '':
        smtp.login(username, password)

    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

parser = argparse.ArgumentParser()
parser.add_argument('attachment')
args = parser.parse_args()
attachpath = args.attachment

config = configparser.ConfigParser()
config.read('email_file.ini')
email_from = config['DEFAULT']['From']
email_to_list = json.loads(config['DEFAULT']['To'])
email_subject = config['DEFAULT']['Subject']
email_body = config['DEFAULT']['Body']
email_server = config['DEFAULT']['Server']
email_server_ssl = bool(config['DEFAULT']['Server_SSL'])
email_server_username = config['DEFAULT']['Server_Username']
email_server_password = config['DEFAULT']['Server_Password']

send_mail(email_from, email_to_list, email_subject, email_body, [attachpath], email_server, email_server_ssl, email_server_username, email_server_password)
