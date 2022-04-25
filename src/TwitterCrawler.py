#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from Utils import *
from time import sleep
import csv

CHROME_DRIVER_PATH = "./chromedriver"
TWITTER_USERNAME_EMAIL = "username_here"
TWITTER_USERNAME_PASSWORD = "pw_here"
TWITTER_URL_TO_SCRAPE = "https://twitter.com/cristiano"
TWIT_COUNT_TO_SCRAPE = 15
# above lines need to be updated

TWITTER_LOGIN_URL = "https://twitter.com/login"

# PAGE SOURCE CLASS PATH, XPATH
LOGIN_USERNAME_ELEMENT_NAME_ATTRIBUTE = "text"
NEXT_BUTTON_ELEMENT_XPATH = "//*[contains(text(), 'Next')]"
LOGIN_PASSWORD_ELEMENT_NAME_ATTRIBUTE = "password"
LOGIN_BUTTON_ELEMENT_XPATH = '//div[@data-testid="LoginForm_Login_Button"]'


class TwitterCrawler:
    def __init__(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)
        self.driver.set_page_load_timeout(15)

    def run(self):
        self.driver.get(TWITTER_LOGIN_URL)
        #self.login()
        twit_set = self.collect_twits()
        self.print_twits_line_by_line(twit_set)
        self.driver.close()

    def login(self):
        ## Find and fill the email field
        element_email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, LOGIN_USERNAME_ELEMENT_NAME_ATTRIBUTE))
        )
        element_email_field.send_keys(TWITTER_USERNAME_EMAIL)

        next = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, NEXT_BUTTON_ELEMENT_XPATH))
        )
        next.click()




        ## Find and fill the password field
        element_password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, LOGIN_PASSWORD_ELEMENT_NAME_ATTRIBUTE))
        )
        element_password_field.send_keys(TWITTER_USERNAME_PASSWORD)

        # Find and click the login button
        self.driver.find_element_by_xpath(LOGIN_BUTTON_ELEMENT_XPATH).click()

        sleep(5)

    def collect_twits(self):
        with open('twits.csv', mode='w') as csv_file:
            fieldnames = ['retwit', 'likes', 'comments', 'content']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

        self.driver.get(TWITTER_URL_TO_SCRAPE)
        twit_set = set()
        while True:
            sleep(5)
            self.scroll_down_to_bottom()
            content = self.get_dynamic_content_of_page()
            twits_in_one_page = find_all_between(
                'div class="css-1dbjc4n"><div aria-label="',
                '"Share Tweet" ', content)
            for twit in twits_in_one_page:
                numbers = find_all_between('div class="css-1dbjc4n r-18u37iz r-1h0z5md"><div aria-label="', '.', twit)

                try :
                    replies = numbers[0]
                except:
                    continue

                if 'Replies' not in replies:
                    continue
                retwit = numbers[1]
                likes = numbers[2]

                twit_content = find_between(
                    '<div class="css-1dbjc4n"><div class="css-1dbjc4n"><div lang="en" dir="auto" class="css-901oao r-1nao33i',
                    '</span>', content)
                twit_content = str_after(twit_content, '<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">')

                #twit_set.add(clean_html(twit))

                if twit_content in twit_set:
                    continue

                twit_set.add(twit_content)



                with open('twits.csv', mode='a') as csv_file:
                    fieldnames = ['replies', 'retwit', 'likes', 'content']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writerow({'replies': retwit, 'retwit': retwit, 'likes': likes, 'content': twit_content})

            if TWIT_COUNT_TO_SCRAPE < len(twit_set):
                with open("ronaldo.html", "a") as my_file:
                    my_file.write(content)

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
