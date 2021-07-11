# Send recap notification

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
from decouple import config
import os.path

# from https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
def send_output():

    fromaddr = "emu-fmnh@fieldmuseum.org"
    toaddr = "emu-fmnh@fieldmuseum.org"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = 'EMu: Output from emu_xml_to_json'

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    if os.path.isfile(config('OUT_PATH') + 'xml_log_' + str(date.today()) + '.txt'):
        body = 'EMu error-log from emu_xml_to_json for ' + str(date.today())
        filename1 = config('OUT_PATH') + 'xml_log_' + str(date.today()) + '.txt'
        attachment1 = open(filename1, "rb")

        # To change the payload into encoded form
        p.set_payload((attachment1).read())

        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

    if os.path.isfile(config('OUT_PATH') + 'emu_to_json.json'):
        body = 'EMu json-output from emu_xml_to_json for ' + str(date.today())
        filename2 = config('OUT_PATH') + 'emu_to_json.json'
        attachment2 = open(filename2, "rb")
        # To change the payload into encoded form
        p.set_payload((attachment2).read())

        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
    
    msg.attach(MimeText(body, 'plain'))
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(fromaddr, config('FROM_PW'))
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    
    # terminating the session
    s.quit()


if __name__ == '__main__':
    send_output()