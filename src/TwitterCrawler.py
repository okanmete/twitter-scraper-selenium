#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from Utils import *
from time import sleep

CHROME_DRIVER_PATH = "CHROME_DRIVER_PATH"
TWITTER_USERNAME_EMAIL = "YOUR_TWITTER_USERNAME_OR_EMAIL"
TWITTER_USERNAME_PASSWORD = "YOUR_TWITTER_PASSWORD"
TWITTER_URL_TO_SCRAPE = "https://twitter.com/cristiano"
TWIT_COUNT_TO_SCRAPE = 15
# above lines need to be updated

TWITTER_LOGIN_URL = "https://twitter.com/login"

# PAGE SOURCE CLASS PATH, XPATH
LOGIN_USERNAME_ELEMENT_NAME_ATTRIBUTE = "session[username_or_email]"
LOGIN_PASSWORD_ELEMENT_NAME_ATTRIBUTE = "session[password]"
LOGIN_BUTTON_ELEMENT_XPATH = '//div[@data-testid="LoginForm_Login_Button"]'


class TwitterCrawler:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)
        self.driver.set_page_load_timeout(15)

    def run(self):
        self.driver.get(TWITTER_LOGIN_URL)
        self.login()
        twit_set = self.collect_twits()
        self.print_twits_line_by_line(twit_set)
        self.driver.close()

    def login(self):
        ## Find and fill the email field
        element_email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, LOGIN_USERNAME_ELEMENT_NAME_ATTRIBUTE))
        )
        element_email_field.send_keys(TWITTER_USERNAME_EMAIL)

        ## Find and fill the password field
        element_password_field = self.driver.find_element_by_name(LOGIN_PASSWORD_ELEMENT_NAME_ATTRIBUTE)
        element_password_field.send_keys(TWITTER_USERNAME_PASSWORD)

        # Find and click the login button
        self.driver.find_element_by_xpath(LOGIN_BUTTON_ELEMENT_XPATH).click()

    def collect_twits(self):
        self.driver.get(TWITTER_URL_TO_SCRAPE)
        twit_set = set()
        while True:
            sleep(2)
            self.scroll_down_to_bottom()
            content = self.get_dynamic_content_of_page()
            twits_in_one_page = find_all_between(
                'r-bnwqim r-qvutc0"><span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">',
                '</path>', content)
            for twit in twits_in_one_page:
                twit_set.add(clean_html(twit))
            if TWIT_COUNT_TO_SCRAPE < len(twit_set):
                break
        return twit_set

    def get_dynamic_content_of_page(self):
        return self.driver.execute_script("return document.body.innerHTML")

    def scroll_down_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def print_twits_line_by_line(self, twit_set):
        for twit in twit_set:
            print(twit)


if __name__ == '__main__':
    twitter_crawler = TwitterCrawler()
    twitter_crawler.run()
