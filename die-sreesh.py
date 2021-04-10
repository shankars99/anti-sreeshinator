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
contact, text = send_message()

startup()
gotoSearchBar(driver, contact)
while( True ):
    #getChatMessage(driver, contact, text)
    getChatMessageTest(driver, contact, text)
    quitApp(driver)
