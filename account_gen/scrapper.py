
from selenium import webdriver  # pip3 install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import time, random, uuid, threading

DRIVER_PATH = "./chromedriver"

LOGIN_URL = "https://discord.com/register?email="


def generate_uid():
    return uuid.uuid4()

def driver_connect():
    options = Options()
    # options.add_argument("--window-size=1920x1080")
    options.add_argument("--start-maximized")
    options.add_argument("--verbose")
    options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"
    # options.add_argument("--headless")
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def random_sleep():
    second = random.randint(5, 7)
    time.sleep(second)

def sleep(second):
    time.sleep(second)


def navigation(driver, url):
    driver.get(url)
    random_sleep()

def if_exist(driver, type, name):
    try:
        match type:
            case 'id':
                return driver.find_element(By.ID, name)
            case 'class':
                return driver.find_element(By.CLASS_NAME, name)
            case 'css_selector':
                return driver.find_element(By.CSS_SELECTOR, name)
            case 'xpath':
                return driver.find_element(By.XPATH, name)
    except:
        return False
        
def login(driver, user):

    print(f'@ Login to the account {user["email"]}')

    # Insert username
    username_element = driver.find_element(By.NAME, "username")
    username_element.send_keys(user["username"])

    # Insert password
    mdp_element = driver.find_element(By.NAME, "password")
    mdp_element.send_keys(user["password"])

    # Day birthday
    # day_element_wrapper = driver.find_element(By.XPATH, "//div[contains(@class, 'day-')]")
    # print('=========== DAY ============')
    # print(day_element_wrapper.get_attribute('innerHTML'))
    # day_select_element = day_element_wrapper.find_element(By.XPATH, "//div[contains(@class, '-placeholder')]")
    # print(day_select_element.get_attribute('innerHTML'))
    # day_button = driver.find_element(By.CSS_SELECTOR, "div.day-1uOKpp > div > div > .css-1kj8ui-container")
    day_button = driver.find_element(By.ID, "react-select-3-input")
    print(day_button.get_attribute('innerHTML'))
    driver.execute_script("arguments[0].click();", day_button)
    raise Exception()

    day_select = driver.find_element(By.CSS_SELECTOR, "div.day-1uOKpp > div > div > div > div > div > .css-o3gndj-placeholder")
    driver.execute_script(f"arguments[0].innerText = '" + user["day_birthday"] + "'", day_select)

    # Month birthday
    # month_element_wrapper = driver.find_element(By.XPATH, "//div[contains(@class, 'month-')]")
    # print('=========== MONTH ============')

    # print(month_element_wrapper.get_attribute('innerHTML'))

    # month_select_element = month_element_wrapper.find_element(By.XPATH, "//div[contains(@class, '-placeholder')]")
    # print(month_select_element.get_attribute('innerHTML'))
    month_select = driver.find_element(By.CSS_SELECTOR, "div.month-1Z2bRu > div > div > div > div > div > .css-o3gndj-placeholder")
    driver.execute_script(f"arguments[0].innerText = '" + user["month_birthday"] + "'", month_select)

    # Year birthday
    # year_element_wrapper = driver.find_element(By.XPATH, "//div[contains(@class, 'year-')]")
    # print('=========== YEAR ============')
    # print(year_element_wrapper.get_attribute('innerHTML'))

    # year_select_element = year_element_wrapper.find_element(By.XPATH, "//div[contains(@class, '-placeholder')]")
    # print(year_select_element.get_attribute('innerHTML'))
    year_select = driver.find_element(By.CSS_SELECTOR, "div.year-3_SRuv > div > div > div > div > div > .css-o3gndj-placeholder")
    driver.execute_script(f"arguments[0].innerText = '" + user["year_birthday"] + "'", year_select)

    # Click on Login Button 
    submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'button-')]")
    print(submit_button.get_attribute('innerHTML'))
    driver.execute_script("arguments[0].click();", submit_button)

    raise Exception()
    random_sleep()

def main():

    driver = driver_connect()

    user = {
        "email": "jeremyluzon@gmail.com",
        "email_url": "jeremyluzon%40gmail.com",
        "username": "jeremytesting",
        "password": "1234567@testing",
        "day_birthday": "15",
        "month_birthday": "August",
        "year_birthday": "1997"
    }

    navigation(driver, LOGIN_URL + user['email_url'])

    login(driver, user)

    







# Main Function
if __name__ == '__main__':
    main()