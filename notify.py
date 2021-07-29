# send notification
# based on https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server


# import email, smtplib, ssl

# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# from decouple import config
# from datetime import date, datetime


import os

def send_output(message, subject, filename, to):
    if len(filename) > 0:
        notify = 'echo ' + message + " | mutt -s " + subject + " -a " + filename + " " + to 
    
    else:
        notify = 'echo ' + message + " | mutt -s " + subject + " " + to

    os.system(notify)


# # don't use this if port 25 is blocked
# def send_output_gmail(send_date=str(date.today()), send_time=str(datetime.now()), send_msg="", filename="", to="", fro=""):

#     subject = "EMu xml-to-json results - " + send_date
#     body = "Output from EMu-xml-to-json - " + send_time + " - log: \n" + send_msg
#     # password = ""

#     # Create a multipart message and set headers
#     message = MIMEMultipart()
#     message["From"] = fro
#     message["To"] = to
#     message["Subject"] = subject

#     # Add body to email
#     message.attach(MIMEText(body, "plain"))

#     if len(filename) > 0:
#         # filename = "data_out/emu_to_json.json"  # In same directory as script

#         # Open attachment-file in binary mode
#         with open(filename, "rb") as attachment:
#             # Add file as application/octet-stream
#             # Email client can usually download this automatically as attachment
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(attachment.read())

#         # Encode file in ASCII characters to send by email    
#         encoders.encode_base64(part)

#         # Add header as key/value pair to attachment part
#         part.add_header(
#             "Content-Disposition",
#             f"attachment; filename= {filename}",
#         )

#         # Add attachment to message and convert message to string
#         message.attach(part)
#         text = message.as_string()

#     # Log in to server using secure context and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP("aspmx.l.google.com:25") as server:
#     # with smtplib.SMTP_SSL("aspmx.l.google.com", 25, context=context) as server:
#     # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         # server.login(sender_email, password)
#         # server.sendmail(sender_email, receiver_email, text)
#         server.send_message(message)


if __name__ == '__main__':
    send_output()