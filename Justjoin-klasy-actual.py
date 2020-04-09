from selenium import webdriver
import time
import getpass
import datetime
import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
from selenium.webdriver import ActionChains


class Scraper():

    
    def __init__(self, pages_100 = True, login = False):
        self.pages_100 = pages_100
        self.login = login
        gecko_path = r'C:/Users/Michal_schudnij/Desktop/Webscraping/class7/geckodriver'
        url = 'https://justjoin.it/'
        options = webdriver.firefox.options.Options()
        options.headless = True
        self.driver = webdriver.Firefox(options = options, executable_path = gecko_path)
        self.driver.get(url)
        if login == True:
            self.log_in()
			
    def log_in(self):
        self.driver.find_element_by_xpath('//button/span[@class="MuiFab-label"][text()="Sign in"]').click()
        self.driver.find_element_by_xpath('//span[@class="MuiButton-label"][text()="Sign in as Developer"]').click()
        time.sleep(2)
        username = self.driver.find_element_by_xpath('//input[@name="email"]')
        my_email = input('Please provide your email:')
        username.send_keys(my_email)
        time.sleep(5)
        password = self.driver.find_element_by_xpath('//input[@name="password"]')
        my_pass = getpass.getpass('Please provide your password:')
        password.send_keys(my_pass)
        time.sleep(5)
        self.driver.find_element_by_xpath('//button/span[@class="MuiFab-label"][text()="Sign in"]').click()
        time.sleep(5)
    
    def location(self):
        self.driver.find_element_by_xpath('//span[@class="css-mudjgk"][text()="Job offers"]').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//div[@class="css-son5n9"][text() = "offers with salary"]').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//span[@class="MuiButton-label"][text() = "Location"]').click()
        time.sleep(5)
        choose_location = input('Choose location (in Polish):\n')
        ## dodać wszystkie miasta
        if (choose_location in ['Warszawa', 'Kraków', 'Wrocław', 'Poznań', 'Trójmiasto']):
            self.driver.find_element_by_xpath(f'//span[@class="MuiButton-label"][text() = "{choose_location}"]').click()
        else: print('There is no such location')
        #     skill.send_keys(Keys.ENTER)
        time.sleep(15)
    
    def salary(self):
        try:
            self.driver.find_element_by_xpath('//span[@class="css-1fptokh"][text() = "More filters"]').click()
            time.sleep(5)
        except:
            self.driver.find_element_by_xpath('//button/span[@class="MuiFab-label"][text()="Sign in"]').click()
            time.sleep(5)
            self.driver.find_element_by_xpath('//span[@class="css-1fptokh"][text() = "More filters"]').click()
            time.sleep(5)
        min_salary = int(input('Choose minimum salary expectations:\n'))
        max_salary = int(input('Choose maximum salary expectations:\n'))
        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="0"]')
        move1 = ActionChains(self.driver)
        move1.click_and_hold(en).move_by_offset(11 * min_salary / 1000, 0).release().perform()
        time.sleep(30)
        en =  self.driver.find_element_by_xpath('//span[@class="MuiSlider-thumb MuiSlider-thumbColorSecondary"][@data-index="1"]')
        move2 = ActionChains(self.driver)
        move2.click_and_hold(en).move_by_offset(11 * (max_salary - 50000) / 1000, 0).release().perform()
        time.sleep(30)
        self.driver.find_element_by_xpath('//span[@class="MuiButton-label"][text() = "Show offers"]').click()
        time.sleep(5)        

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
        
#     if __name__ == '__main__':
#         if (login == False):
#             login()
#         location()
#         salary()
#         offers()
        
c = Scraper(pages_100 = True, login = False)
c.location()
c.salary()
c.offers()
c.__del__()
