from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import json

#get the contact name and path to webdriver
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

#find the xpath element from the give xpath
def x_path_dest(driver, xpath):
    try:
        xpath_ele = driver.find_element_by_xpath(xpath)
        return xpath_ele
    except NoSuchElementException:
        return None

#navigate to the search bar to find the chat
def gotoSearchBar(driver, contact):
    input_box_search = x_path_dest(driver,
                                   "//*[@id = \"side\"]/div[1]/div/label/div/div[2]")
    input_box_search.click()
    time.sleep(1)
    input_box_search.send_keys(contact)
    time.sleep(1)

#enter the char
def gotoChat(driver, contact):
    selected_contact = driver.find_elements_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()

#incase you want to send a message
def sendMessage(driver, contact, text):
    gotoChat(driver, contact)
    input_box = x_path_dest(driver,
                            "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]")
    time.sleep(1)
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(1)

#create a list and append the newest messages after a cycle of parsing through the older messages
def logChatMessage(driver, contact):
    last_message = ['The List']

    #goto the contact in whatsapp
    selected_contact = driver.find_element_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()

    #some xpath stuff to find the message in the html spam
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

#go through the last block of messages and extract the last sent message
def extractLastMessage(driver, prefix, msg_types, msg_num_postNum, last_message):
    for num in range(30, 0, -1):
        msg_prefix = prefix + str(num) + msg_num_postNum
        for msg_type in msg_types:
            temp_last_message = showMessage(x_path_dest(driver, msg_prefix + msg_type))

            #check if the message is already logged, if not add to list
            if temp_last_message not in last_message:
                last_message.append(temp_last_message)
                print(temp_last_message)
                return


def showMessage(input_box):
    try:
        if input_box != None and input_box.get_attribute("data-pre-plain-text") != None:
            sender = input_box.get_attribute("data-pre-plain-text")
            message = input_box.text
            send_message = (sender + message)
            return send_message
        else:
            return 'The List'
    except StaleElementReferenceException:
        return 'The List'

def quitApp(driver):
    print("quit?")
    if input() == 'y':
        driver.quit()
