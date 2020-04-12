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
    def __init__(self, headless_mode = True, pages_100 = True, choose_location = False, choose_salary = False):
        self.pages_100 = pages_100
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

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-son5n9"][text() = "offers with salary"]')))
        element.click()

        if choose_location == True:
            self.location()
        if choose_salary == True:
            self.salary()




    def location(self):
        
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
        # element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.css-1fptokh')))
        
        # element = self.driver.find_elements_by_css_selector("#root > div.css-gwbava > div > div.css-1myb1t6 > button > span.MuiButton-label > span.css-1fptokh")
        # self.driver.find_element_by_xpath('//button/span[text() = "More filters"]').click()
        
        ##### PROBLEM TUTAJ ####
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@tabindex="0"]')))
        element.click()

        # user inputs
        min_salary = int(input('Choose minimum salary expectations:\n'))
        max_salary = int(input('Choose maximum salary expectations:\n'))

        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="0"]')
        # swipe horizontal slider due to user input (left-hand edge)
        move_left = ActionChains(self.driver)
        move_left.click_and_hold(en).move_by_offset(11 * min_salary / 1000, 0).release().perform()

        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="1"]')
        # swipe horizontal slider due to user input (right-hand edge)
        move_right = ActionChains(self.driver)
        move_right.click_and_hold(en).move_by_offset(11 * (max_salary - 50000) / 1000, 0).release().perform()

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
        

c = Scraper(headless_mode = False, pages_100 = False, choose_location = True, choose_salary = True)

links = c.offers()
for link in links:
    print(link)
c.__del__()
