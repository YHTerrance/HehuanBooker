from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from config import person, TESSERACT_PATH, CHROME_DRIVER_PATH, TARGET_URL

import time
import pytesseract
import re
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def replace_chars(text):
    """
    Replaces all characters instead of numbers from 'text'.

    :param text: Text string to be filtered
    :return: Resulting number
    """
    list_of_numbers = re.findall(r'\d+', text)
    result_number = ''.join(list_of_numbers)
    return result_number


def get_captcha(driver, element, path):
    # now that we have the preliminary stuff
    # out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot("screenshot.png")

    # uses PIL library to open image in memory
    image = Image.open("screenshot.png")

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path)  # saves new cropped image


if __name__ == "__main__":

    start_time = time.time()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--force-device-scale-factor=1')

    browser = webdriver.Chrome(
        options=options,
        executable_path=CHROME_DRIVER_PATH)

    browser.get(TARGET_URL)

    browser.set_window_size(1024, 768)

    browser.find_element_by_id("accept").click()
    browser.find_element_by_id("btn_agree").click()

    browser.switch_to.alert.accept()

    browser.find_element_by_id("user").send_keys(person["account"])
    browser.find_element_by_id("password").send_keys(person["password"])

    img = browser.find_element_by_xpath('''//*[@id="form"]/table/tbody/tr[2]/td/table/
    tbody/tr[4]/td/img''')

    get_captcha(browser, img, "captcha.png")

    # Grayscale image
    img = Image.open('captcha.png').convert('L')
    ret, img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)

    # Older versions of pytesseract need a pillow image
    # Convert back if needed
    img = Image.fromarray(img.astype(np.uint8))

    captcha = pytesseract.image_to_string(
            img,
            lang="eng", config='''--psm 7 -c
            tessedit_char_whitelist=0123456789''')

    captcha = replace_chars(captcha)

    print("Captcha number:", captcha)

    browser.find_element_by_id("verifycode").send_keys(captcha)

    browser.find_element_by_xpath(
        '''//*[@id="form"]/table/tbody
        /tr[2]/td/table/tbody/tr[5]/td/img
        ''').click()

    browser.find_element_by_id("stay_id").send_keys(person["id"])
    browser.find_element_by_id("stay_name").send_keys(person["name"])
    browser.find_element_by_id("stay_car_plate").send_keys(person["car_plate"])
    browser.find_element_by_id("stay_mobile").send_keys(person["mobile"])
    browser.find_element_by_id("stay_email").send_keys(person["email"])
    browser.find_element_by_id("next").click()

    browser.find_element_by_xpath(f'''//*
        [@id="hotel_category"]/dl[{person
        ["forest_park"]}]/dd[2]/input''').click()
    browser.find_element_by_id("next").click()

    url = browser.current_url
    newurl = url+f"&year=2021&m={person['month']}"
    browser.get(newurl)

    # Explicit wait
    desired_date_xpath = f'''//
    input[@value={person["date"]}
    ]'''

    wait = WebDriverWait(browser, 5)
    element = wait.until(EC.element_to_be_clickable((
        By.XPATH,                   desired_date_xpath)))

    browser.find_element_by_xpath(desired_date_xpath).click()

    browser.find_element_by_id("next").click()

    print("Spent time:", time.time() - start_time)
