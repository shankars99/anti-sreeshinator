from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

import time
import json

f = open("conf.json", "r")
data = json.loads(f.read())

def get_group_name():
    contact = data["contact"]
    return contact


def driver_init(url):
    driver = webdriver.Firefox(executable_path=data["driver_path"])
    driver.get(url)
    return driver


def startup():
    print("Scan QR Code, And then Enter")
    input()
    print("Logged In")


def x_path_dest(driver, xpath):
    try:
        xpath_res = driver.find_element_by_xpath(xpath)
        return xpath_res
    except NoSuchElementException:
        return None


def gotoSearchBar(driver, contact):
    input_box_search = x_path_dest(driver,
                                   "//*[@id = \"side\"]/div[1]/div/label/div/div[2]")
    input_box_search.click()
    time.sleep(1)
    input_box_search.send_keys(contact)
    time.sleep(1)


def gotoChat(driver, contact):
    selected_contact = driver.find_elements_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()


def sendMessage(driver, contact, text):
    gotoChat(driver, contact)
    input_box = x_path_dest(driver,
                            "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]")
    time.sleep(1)
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(1)


def getChatMessage(driver, contact):
    selected_contact = driver.find_element_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()

    for num in range(30, 1, -1):

        input_box = x_path_dest(driver,
                                "//*[@id=\"main\"]/div[3]/div/div/div[3]/div["+str(num)+"]/div/div/div/div")
        if input_box != None and input_box.get_attribute("data-pre-plain-text") != None:
            print(input_box.get_attribute(
                "data-pre-plain-text") + input_box.text + "\n")
        else:
            pass


def getChatMessageTest(driver, contact):
    last_message = ['The List']
    selected_contact = driver.find_element_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()

    prefix = "//*[@id=\"main\"]/div[3]/div/div/div[3]/div["
    msg_num_postNum = "]/div/div/"

    fwd = "div/div[3]"
    reply = "div[2]/div[2]"
    first = "div/div[2]"
    notFirst = "div/div[1]"

    msg_types = [notFirst, reply, first, fwd]

    while True:
        extractLastMessage(driver, prefix, msg_types,
                           msg_num_postNum, last_message)


def extractLastMessage(driver, prefix, msg_types, msg_num_postNum, last_message):
    for num in range(30, 0, -1):
        msg_prefix = prefix + str(num) + msg_num_postNum
        for msg_type in msg_types:
            temp_last_message = showMessage(x_path_dest(driver, msg_prefix + msg_type))

            if temp_last_message not in last_message:
                last_message.append(temp_last_message)
                print(temp_last_message)
                return


def showMessage(input_box):
    if input_box != None and input_box.get_attribute("data-pre-plain-text") != None:
        sender = input_box.get_attribute("data-pre-plain-text")
        message = input_box.text
        send_message = (sender + message)
        return send_message
    else:
        return 'The List'


def quitApp(driver):
    print("quit?")
    if input() == 'y':
        driver.quit()
