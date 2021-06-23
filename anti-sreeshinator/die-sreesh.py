from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import time
from lambsauce import *


url = "https://web.whatsapp.com"

driver = driver_init(url)
contact= get_group_name()

startup()
gotoSearchBar(driver, contact)

option = input("1.Log messages\n2.Send a message\nEnter your choice:")
if option == '1':
    logChatMessage(driver, contact)
else:
    msg = input("Enter message to be sent:")
    sendMessage(driver, contact, msg)
