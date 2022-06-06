
from selenium import webdriver  # pip3 install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import anticaptchaofficial.hcaptchaproxyless as anticaptcha # pip3 install anticaptchaofficial


import time
import random
import uuid
import threading
import requests # pip3 requests
import json
import re
import os
import zipfile

DRIVER_PATH = "./chromedriver"

LOGIN_URL = "https://discord.com/register?email="

PROXY_MANIFEST = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
"""

PORXY_AUTH_PLUGIN = 'proxy_auth_plugin.zip'

def generate_uid():
    return uuid.uuid4()

def getter_proxy():
    proxies = []
    with open('../data/proxies.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            proxies.append(line.replace('\n', ''))
    return proxies

def driver_connect():
    proxies = getter_proxy()

    print("proxies.length : " + str(len(proxies)))
    selected_proxy = random.choice(proxies)
    proxy_data = selected_proxy.split('@')
    proxy_auth = proxy_data[0]
    proxy_host = proxy_data[1]
    options = Options()
    # options.add_argument("--window-size=1920x1080")
    options.add_argument("--start-maximized")
    options.add_argument("--verbose")
    options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"


    # Proxy use : 
    background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
    """ % (proxy_host.split(':')[0], proxy_host.split(':')[1], proxy_auth.split(':')[0], proxy_auth.split(':')[1])
    with zipfile.ZipFile(PORXY_AUTH_PLUGIN, 'w') as zp:
        zp.writestr("manifest.json", PROXY_MANIFEST)
        zp.writestr("background.js", background_js)
    options.add_extension(PORXY_AUTH_PLUGIN)
    # options.add_argument('--proxy-server=%s' % selected_proxy)
    # options.add_argument("--headless")
    # options.add_extension('./plugin.zip')
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

def form_submit(driver, token):
    print('form_submit')

    print(f'Token : {token}')

    # driver.execute_script("grecaptcha.getResponse = function(){return '{}'}".format(token))

    # # driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(token))
    # # driver.execute_script("grecaptcha.recaptchaCallback[0]('{}')".format(token))
    # captcha_element = driver.find_element(By.NAME, "h-captcha-response")
    # print(captcha_element.get_attribute("innerHTML"))
    # print(captcha_element)
    # driver.execute_script("arguments[0].innerHTML = arguments[1]", captcha_element, token)
    # print('after first script')
    # driver.execute_script("grecaptcha.recaptchaCallback[0]('{}')".format(token))
    driver.execute_script("document.getElementsByName('h-captcha-response')[0].style = 'width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px;';")
    # print('after first script')
    driver.find_element(By.NAME,'h-captcha-response').send_keys(token)
    # print('after second script')

    driver.execute_script("document.getElementsByName('g-recaptcha-response')[0].style = 'width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px;';")
    # print('after third script')
    driver.find_element(By.NAME,'g-recaptcha-response').send_keys(token)
    # print('after fourth script')
    random_sleep()

def solve_captcha(driver):
    apiKey = "2a6b07b13f06fc3123da2d8f58168978"
    pattern_sitekey = "&sitekey=(.*?)&"
    src = driver.find_element(By.CSS_SELECTOR, 'iframe').get_attribute("src")
    sitekey = re.search(pattern_sitekey, src).group(1)
    solver = anticaptcha.hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key(apiKey)
    solver.set_website_url("https://discord.com")
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()
    form_submit(driver, g_response)
    # bypass(sitekey, "discord.com", proxy="xyliase:k3QsT6SBGD@45.11.21.102:5500")
    # print('before plugin')
    # webdriver.support.wait.WebDriverWait(driver, 120).until(lambda x: x.find_element(By.CSS_SELECTOR, '.antigate_solver.solved'))
    # print('after plugin')

def get_email():
    url = "https://gmailnator.p.rapidapi.com/generate-email"

    payload = {"options": [1, 2, 3]}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "gmailnator.p.rapidapi.com",
        "X-RapidAPI-Key": "e2adfb4001mshca28efd840b367ap1ccb61jsnf3bd380d2f5c"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.json():
        return response.json()['email']
    # return 'test_last_time@gmail.com'

def get_email_inbox(user):
    url = "https://gmailnator.p.rapidapi.com/inbox"

    payload = {
        "email": user['email'],
        "limit": 10
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "gmailnator.p.rapidapi.com",
        "X-RapidAPI-Key": "e2adfb4001mshca28efd840b367ap1ccb61jsnf3bd380d2f5c"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())


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

    # Insert email
    username_element = driver.find_element(By.NAME, "email")
    username_element.send_keys(user["email"])

    # Insert username
    username_element = driver.find_element(By.NAME, "username")
    username_element.send_keys(user["username"])

    # Insert password
    mdp_element = driver.find_element(By.NAME, "password")
    mdp_element.send_keys(user["password"])

    actions = ActionChains(driver)
    time.sleep(.5)

    # Locating to the first date input then the discord will navigate the focuse to the next input
    driver.find_element(By.CLASS_NAME, 'css-1hwfws3').click()
    actions.send_keys(user["month_birthday"])  # Submitting the month
    actions.send_keys(Keys.ENTER)

    actions.send_keys(str(random.randint(1, 28)))  # Submitting the day

    actions.send_keys(Keys.ENTER)

    actions.send_keys(str(random.randint(1990, 2001)))  # Submitting the year

    actions.send_keys(Keys.ENTER)

    actions.send_keys(Keys.TAB)  # Navigating to continue button

    actions.send_keys(Keys.ENTER)  # Creates the account

    actions.perform()  # All the actions are pending and needs to perform all at once

    random_sleep()


def main():


    driver = driver_connect()

    email = get_email()

    user = {
        "email": email,
        "username": "jeremytesting",
        "password": "1234567@testing",
        "day_birthday": "15",
        "month_birthday": "August",
        "year_birthday": "1997"
    }

    navigation(driver, LOGIN_URL)

    login(driver, user)

    solve_captcha(driver)

    print('after solve_captcha')
    random_sleep()

    print('after sleep')
    get_email_inbox(user)

    print('after get_email_inbox')

    random_sleep()

    raise Exception()

# Main Function
if __name__ == '__main__':
    main()
