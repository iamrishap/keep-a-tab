import base64
from getpass import getpass
import os


def check_config_exists():
    if not os.path.isfile('stages_config.txt'):
        return False
    with open('stages_config.txt', 'r+') as config_handler:
        if 'FINISH' not in config_handler.read():
            config_handler.truncate(0)
            return False
        else:
            return True


def clear_search_config():
    global config_handler
    config_handler.truncate(0)


def create_search_config():
    global config_handler
    config_handler = open('stages_config.txt', 'w+')
    step_choice = None
    step_possibilities = """
        1. Go to a URL
        2. Input a text in textbox
        3. Click on a button
        4. Enter text in a textbox
        5. Click on an anchor(link)
        6. Search a text
        7. Send a text message
        8. Send an email
        9. Finish the flow
        10. Delete and start again
        11. Exit(without saving)
    """
    try:
        while step_choice != '11' or step_choice != '9':
            print("What do you want this step to do? Choose one of the options below:")
            print(step_possibilities)
            step_choice = input().strip()
            switch_handler(step_choice)
    finally:
        config_handler.close()


def finish_flowchart():
    global config_handler
    finish_config = dict()
    finish_config["type"] = 'FINISH'
    config_handler.write(str(finish_config))
    print("Steps complete")


def get_anchor_click_details():
    global config_handler
    anchor_config = {"type": "anchor"}
    print("To uniquely identify the anchor, one the the identifier among id or anchor text.")
    print("What is the anchor id? Press enter if it's absent.")
    anchor_id = input().strip()
    if anchor_id != '':
        anchor_config["id"] = anchor_id
    print("What is the text written on the anchor? Press enter if it's absent.")
    anchor_text = input().strip()
    if anchor_text != '':
        anchor_config["text"] = anchor_text
    if not anchor_id and not anchor_text:
        print("Can't create the anchor config without any identifier. Exiting!")
        exit(0)
    config_handler.write(str(anchor_config) + "\r\n")
    print("Anchor config saved.\r\n\r\n")


def get_button_click_details():
    global config_handler
    print("\r\n---------------- Button config ----------------")
    button_config = {"type": "button"}
    print("To uniquely identify the button, one the the identifier among id, name, value, text is required.")
    print("What is the button id? Press enter if it's absent.")
    button_id = input().strip()
    if button_id != '':
        button_config["id"] = button_id
    print("What is the button name? Press enter if it's absent.")
    button_name = input().strip()
    if button_name != '':
        button_config["name"] = button_name
    print("What is the button value? Press enter if it's absent.")
    button_value = input().strip()
    if button_value != '':
        button_config["value"] = button_value
    print("What is the button text? Press enter if it's absent.")
    button_text = input().strip()
    if button_text != '':
        button_config["text"] = button_text
    if not button_id and not button_name and not button_value and not button_text:
        print("Can't create the button config without any identifier. Exiting!")
        exit(0)
    config_handler.write(str(button_config) + "\r\n")
    print("Button config saved.\r\n\r\n")


def get_email_sending_details():
    global config_handler
    email_config = {"type": "email"}
    print("\r\n---------------- Gmail email config ----------------")
    print("What is the Subject for the email that you want to send?")
    subject = input().strip()
    if subject != '':
        email_config["subject"] = subject
    print("What is the email message you want to send?")
    message = input().strip()
    if message != '':
        email_config["message"] = message
    print("Who should the email be sent to?")
    recipient_email = input().strip()
    if recipient_email != '':
        email_config["receiver"] = recipient_email
    print("To send the message using Gmail API. Login password is required. It will be stored in an encrypted form.")
    print("What is your Gmail account email ID (sender email)?")
    sender_email = input().strip()
    if sender_email != '':
        email_config["id"] = sender_email
    print("What is the password for {} email ID?".format(sender_email))
    raw_pwd = getpass(prompt="Enter password and then press enter. Input is hidden.")
    byte_pwd = raw_pwd.encode('utf-8')
    password = base64.b64encode(byte_pwd)
    if password != '':
        email_config["password"] = password
    if not subject or not message or not recipient_email or not sender_email or not password:
        print("Can't configure the email config without proper subject, message, "
              "recipient email, sender email and sender password. Exiting!")
        exit(0)
    config_handler.write(str(email_config) + "\r\n")
    print("Button config saved.\r\n\r\n")


def get_mobile_text_details():
    global config_handler
    print("\r\n---------------- Twilio SMS config ----------------")
    message_config = {"type": "message"}
    print("What is the message you want to send?")
    message = input().strip()
    if message != '':
        message_config["message"] = message
    print("Which number to send this message to?")
    number = input().strip()
    if number != '':
        message_config["number"] = number
    print("To send the message using Twilio API. " +
          "Account SID and Auth Token are required. They will be stored in an encrypted form.")
    print("What is your Twilio account SID?")
    account_sid = input().strip()
    if account_sid != '':
        message_config["id"] = account_sid
    print("What is your Twilio account Auth Token?")
    auth_token = input().strip()
    if auth_token != '':
        message_config["name"] = auth_token
    if not account_sid or not auth_token:
        print("Can't configure the messaging config without proper account SID and Auth Token. Exiting!")
        exit(0)
    config_handler.write(str(message_config) + "\r\n")
    print("Button config saved.\r\n\r\n")


def get_search_text():
    global config_handler
    search_config = {"type": "text"}
    print("Enter the text you need to find/not find on the page")
    text = input().strip()
    if text != '':
        search_config["text"] = text
    print("Do you want its existence or absence on the page? Enter 1 for Existence and 2 for Absence.")
    search_config["exists"] = True if input().strip() == '1' else False
    config_handler.write(str(search_config) + "\r\n")
    print("Search config saved.\r\n\r\n")


def get_text_input_details():
    global config_handler
    print("\r\n---------------- Input text config ----------------")
    textbox_config = {"type": "textbox"}
    print("To uniquely identify the textbox, one the the identifier among id, name, placeholder is required.")
    print("What is the textbox id? Press enter if it's absent.")
    textbox_id = input().strip()
    if textbox_id != '':
        textbox_config["id"] = textbox_id
    print("What is the textbox name? Press enter if it's absent.")
    textbox_name = input().strip()
    if textbox_name != '':
        textbox_config["name"] = textbox_name
    print("What is the textbox placeholder or help text? Press enter if it's absent.")
    textbox_placeholder = input().strip()
    if textbox_placeholder != '':
        textbox_config["text"] = textbox_placeholder
    if not textbox_id and not textbox_name and not textbox_placeholder:
        print("Can't create the textbox config without any identifier. Exiting!")
        exit(0)
    print("\r\nConfidential texts are stored in an encrypted format.")
    print("Are you going to input a confidential text? Like account number, password etc? Input 1 for Yes or 2 for No")
    confidential = True if input().strip() == '1' else False
    if confidential:
        raw_text = getpass(prompt="Enter text and then press enter. Input is hidden.")
        byte_text = raw_text.encode('utf-8')
        text = base64.b64encode(byte_text)
        textbox_config["hidden"] = True
    else:
        print("Enter text")
        text = input().strip()
        textbox_config["hidden"] = False
    if text != '':
        textbox_config["filltext"] = text
    config_handler.write(str(textbox_config) + "\r\n")
    print("Textbox config saved.\r\n\r\n")


def navigate_to_url():
    global config_handler
    print("\r\n---------------- Navigation config ----------------")
    nav_config = {"type": "navigate"}
    print("Enter the URL you need to navigate to")
    url = input().strip()
    nav_config["url"] = url
    config_handler.write(str(nav_config) + "\r\n")
    print("Nav config saved.\r\n\r\n")


def read_search_config():
    return open('stages_config.txt', 'r')


def switch_handler(i):
    switch_statement = {
        '1': navigate_to_url,
        '2': get_text_input_details,
        '3': get_button_click_details,
        '4': get_text_input_details,
        '5': get_anchor_click_details,
        '6': get_search_text,
        '7': get_mobile_text_details,
        '8': get_email_sending_details,
        '9': finish_flowchart,
        '10': clear_search_config,
        '11': clear_search_config
    }
    func = switch_statement.get(i, lambda: "Invalid Option")
    return func()
