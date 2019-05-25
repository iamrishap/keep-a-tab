import smtplib
import ssl
from twilio.rest import Client
# import selenium
# import BeautifulSoup4

from flowchart_handler import run_flowchart, show_flowchart
from search_config_handler import check_config_exists, create_search_config, read_search_config
from time import time

config_handler = None
start_time = time()

if __name__ == "___main__":
    config_handler = check_config_exists()
    if not config_handler:
        create_search_config()
    config_handler = read_search_config()
    print("Going to run this flowchart")
    # show_flowchart()
    run_flowchart()
