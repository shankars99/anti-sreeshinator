from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

import time


def send_message():
    contact = "Homo Sapiens"
    text = "Hey, this message was sent using Selenium"
    return contact, text


def driver_init(url):
    driver = webdriver.Firefox(
        executable_path="/home/shankar/Music/geckodriver-v0.29.1-linux32/geckodriver")
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


def getChatMessage(driver, contact, text):
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


def getChatMessageTest(driver, contact, text):
    selected_contact = driver.find_element_by_xpath(
        "//span[@title='"+contact+"']")
    selected_contact.click()

    prefix = "//*[@id=\"main\"]/div[3]/div/div/div[3]/div["
    msg_num_postNum = "]/div/div/"

    fwd = "div/div[3]"
    reply = "div[2]/div[2]"
    first = "div/div[2]"
    notFirst = "div/div[1]"


    last_message = ""
    msg_types = [notFirst, reply, first, fwd]
    for num in range(30, 0, -1):
        msg_prefix = prefix + str(num) + msg_num_postNum
        for msg_type in msg_types:
            temp_last_message = showMessage(x_path_dest(driver, msg_prefix + msg_type), last_message)

            if  last_message != temp_last_message:
                last_message = temp_last_message
                return


def showMessage(input_box, last_message):
    if input_box != None and input_box.get_attribute("data-pre-plain-text") != None:
        sender = input_box.get_attribute("data-pre-plain-text")
        message = input_box.text
        if(sender.find("Sh")) > -1 and message != last_message:
            print(sender + message + "\n")
            return message
    else:
        return last_message


def quitApp(driver):
    print("quit?")
    if input() == 'y':
        driver.quit()
