
# coding: utf-8

# In[66]:


from selenium import webdriver
import time
import getpass
import datetime
import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
from selenium.webdriver import ActionChains


# In[67]:


class Scraper():

    
    def __init__(self, pages_100 = True, login = False):
        self.pages_100 = pages_100
        self.login = login
        gecko_path = r'C:/Users/Michal_schudnij/Desktop/Webscraping/class7/geckodriver'
        url = 'https://justjoin.it/'
        options = webdriver.firefox.options.Options()
        options.headless = False
        self.driver = webdriver.Firefox(options = options, executable_path = gecko_path)
        self.driver.get(url)

        
#     def open_site(self):
#         self.driver.get(url)

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
        self.driver.find_element_by_xpath('//span[@class="MuiButton-label"][text() = "More filters"]').click()
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
        links = []
        # for x in range(1, warunek[if true = 100, if false, niech sobie wybierze uzytkownik])
        for x in range(1,3+1):
            link = self.driver.find_element_by_xpath(f'//div[@class="css-1macblb"]/div/div[{x}]/a').get_attribute("href")
            links.append(link)
            time.sleep(3)
        return links
    
    def __del__(self):
        self.driver.quit()
        
#     if __name__ == '__main__':
#         if (login == False):
#             login()
#         location()
#         salary()
#         offers()
        


# In[68]:


c = Scraper()


# In[69]:


c.log_in()


# In[70]:


c.location()


# In[71]:


c.salary()


# In[72]:


c.offers()


# In[73]:


c.__del__()

