#### DODAC TABS WITH SALARY W KAZDEJ FUNKCJI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import datetime
import os
from os import path
import pandas as pd
import matplotlib.pyplot as plt


class Scraper():

    # declaring options
    def __init__(self, headless_mode = True, pages_100 = True, login = False, choose_location = False, choose_salary = False):
        self.pages_100 = pages_100
        self.login = login
        self.choose_location = choose_location
        self.choose_salary = choose_salary
        self.headless_mode = headless_mode

        # path of geckodriver
        gecko_path = path.join(os.path.dirname(os.path.abspath('__file__')), 'geckodriver')
        url = 'https://justjoin.it/'
        options = webdriver.firefox.options.Options()
        if headless_mode == True:
            options.headless = True
        else:
            options.headless = False
        self.driver = webdriver.Firefox(options = options, executable_path = gecko_path)
        self.driver.get(url)
        if login == True:
            self.log_in()
        if choose_location == True:
            self.location()
        if choose_salary == True:
            self.salary()

    def log_in(self):
        # sign in -> sign in as developer
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button/span[@class='MuiFab-label'][text()='Sign in']")))
        element.click()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text()="Sign in as Developer"]')))
        element.click()
        
        # user inputs
        username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
        my_email = input('Please provide your email:')
        username.send_keys(my_email)
        
        password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
        my_pass = getpass.getpass('Please provide your password:')
        password.send_keys(my_pass)
        
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button/span[@class="MuiFab-label"][text()="Sign in"]')))
        element.click()

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="css-mudjgk"][text()="Job offers"]')))
        element.click()

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-son5n9"][text() = "offers with salary"]')))
        element.click()

    
    def location(self):
        if self.login == True:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Location"]')))
            element.click()
        else:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="css-mudjgk"][text()="Job offers"]')))
            element.click()

            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-son5n9"][text() = "offers with salary"]')))
            element.click()

            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Location"]')))
            element.click()

        # user input
        choose_location = input('Choose location (in Polish):\n')
        ## dodać wszystkie miasta
        if (choose_location in ['Warszawa', 'Kraków', 'Wrocław', 'Poznań', 'Trójmiasto']):
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//span[@class="MuiButton-label"][text() = "{choose_location}"]')))
            element.click()
        else: 
            print('There is no such location. Offers with all possibilities.')
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="MuiButtonBase-root MuiIconButton-root css-tze5xj"]')))
            element.click()

    def salary(self):
        # sometimes window 'sign in' covers 'more filters'
        ## BLAD TU WYSKAKUJE
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button/span[text() = "More filters"]')))
            element.click()
        except:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button/span[@class="MuiButtonBase-root MuiFab-root css-t8t650 MuiFab-extended MuiFab-sizeMedium MuiFab-secondary"][text()="Sign in"]')))
            element.click()
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button/span[text() = "More filters"]')))
            element.click()

        time.sleep(10)
        # user inputs
        min_salary = int(input('Choose minimum salary expectations:\n'))
        max_salary = int(input('Choose maximum salary expectations:\n'))
        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="0"]')
        move1 = ActionChains(self.driver)
        # swipe horizontal slider due to user input (left-hand edge)
        move1.click_and_hold(en).move_by_offset(11 * min_salary / 1000, 0).release().perform()
        time.sleep(30)
        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="1"]')
        move2 = ActionChains(self.driver)
        # swipe horizontal slider due to user input (right-hand edge)
        move2.click_and_hold(en).move_by_offset(11 * (max_salary - 50000) / 1000, 0).release().perform()
        time.sleep(30)    
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Show offers"]')))
        element.click()

    def offers(self):
        if(self.pages_100 == True):
            number = 100
        else:
            ## 5 losowo napisałem, moze niech uzytkownik wprowadzi inuptem?
            number = 5
        
        links = []
        actions = ActionChains(self.driver)

        ## dodać warunek na sytuację, gdy jest mniej niż 100 ofert na stronie!
        while(len(links)<number):
            elements = self.driver.find_elements_by_css_selector("a.css-18rtd1e")

            for element in elements:
                link = element.get_attribute("href")
                if(link in links):
                    continue
                else:
                    links.append(link)
                    if (len(links)>=number):
                        break

            elements[-1].send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
        
        return links
    
    def __del__(self):
        self.driver.quit()
        

c = Scraper(headless_mode = True, pages_100 = False, login = False, choose_location = False, choose_salary = True)

links = c.offers()
for link in links:
    print(link)
c.__del__()
