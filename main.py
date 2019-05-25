import smtplib
import ssl
from twilio.rest import Client
# import selenium
# import BeautifulSoup4

from flowchart import show_flowchart, run_flowchart
from search_config_handler import check_config_exists, create_search_config, read_search_config

config_handler = None


def send_email(message=None, password=None, receiver_email=None, sender_email=None, subject=None):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = """\
    Subject: {0}

    {1}.""".format(subject, message)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Email sent successfully.")
    except:
        print("Exception occurred while trying to send email.")


def send_sms(account_sid, auth_token, message_text, to_number):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message_text,
            from_='+61488843232',
            to=to_number
        )
        print("Message sent successfully with SID: {}".format(message.sid))
    except:
        print("Couldn't send the SMS. API failed.")


if __name__ == "___main__":
    config_handler = check_config_exists()
    if not config_handler:
        create_search_config()
    config_handler = read_search_config()
    print("Going to run this flowchart")
    show_flowchart()
    run_flowchart()
