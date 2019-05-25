from selenium import webdriver
import smtplib
import ssl
from time import time
from twilio.rest import Client
# import BeautifulSoup4

from environment_config import BIN_LOCATION, EXEC_PATH
from search_config_handler import read_search_config

driver = None


def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = BIN_LOCATION
    return webdriver.Chrome(executable_path=EXEC_PATH, chrome_options=options)


def run_flowchart():
    global driver
    driver = get_webdriver()
    steps = read_search_config().readlines().strip()
    for step in steps:
        step_dict = dict(step)
        switch_handler(step_dict["type"], step_dict)


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


def show_flowchart():
    pass


def perform_button_click(args):
    button = None
    if args['id']:  # Prefer ID over name
        button = driver.find_element_by_id(args['id'])
    if args['name'] and not button:
        button = driver.find_element_by_name(args['name'])
    if button:
        button.click()


def perform_anchor_click(args):
    anchor = None
    if args['text']:
        anchor = driver.find_element_by_link_text(args['text'])
    if anchor:
        anchor.click()


def perform_email_sending(args):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = """\
        Subject: {0}

        {1}.""".format(args['subject'], args['message'])
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(args['id'], args['password'])
            server.sendmail(args['id'], args['receiver'], message)
            print("Email sent successfully.")
    except:
        print("Exception occurred while trying to send email.")


def perform_graceful_exit(args):
    global start_time
    print("Flow ran successfully in {} seconds.".format(time() - start_time))


def perform_navigation(args):
    pass


def perform_sms_sending(args):
    client = Client(args['account_sid'], args['auth_token'])
    try:
        message = client.messages.create(
            body=args['message'],
            from_='+61488843232',
            to=args['to_number']
        )
        print("Message sent successfully with SID: {}".format(message.sid))
    except:
        print("Couldn't send the SMS. API failed.")


def perform_text_find(args):
    pass


def perform_text_box_filling(args):
    pass


def switch_handler(type, args):
    switch_statement = {
        'anchor': perform_anchor_click,
        'button': perform_button_click,
        'email': perform_email_sending,
        'FINISH': perform_graceful_exit,
        'navigate': perform_navigation,
        'sms': perform_sms_sending,
        'text': perform_text_find,
        'textbox': perform_text_box_filling,
    }
    func = switch_statement.get(type, lambda: "Invalid Option")
    return func(args)

# python_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
# python_button.click()

# type text
# text_area = driver.find_element_by_id('textarea')
# text_area.send_keys("print('Hello World')")
