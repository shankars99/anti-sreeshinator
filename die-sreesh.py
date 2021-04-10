from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import time




def send_message():
    contact = "me, myself and pi"
    text = "Hey, this message was sent using Selenium"
    return contact, text


def driver_init(url="https://web.whatsapp.com"):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    return driver


def startup():
    print("Scan QR Code, And then Enter")
    input()
    print("Logged In")

def x_path_dest(xpath):
    inp_xpath_search_bar = "/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]"
    xpath_res = driver.find_element_by_xpath(xpath)
    return xpath_res

def getSearchBar():
    input_box_search = x_path_dest(
        "/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]")
    input_box_search.click()
    time.sleep(1)
    input_box_search.send_keys(contact)
    time.sleep(2)

def getChat():
    selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
    selected_contact.click()

    input_box = x_path_dest(
        "/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]")
    time.sleep(2)
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(2)

def quitApp():
    print("quit?")
    if input() == 'y':
        driver.quit()

driver = driver_init()
contact, text = send_message()
