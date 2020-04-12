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
    def __init__(self, headless_mode = True, choose_location = False, choose_salary = False):
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

        """Constructor - declaration of scraper configuration"""
        print("==========================================")
        print("Please, configure scraper!")
        print("==========================================")

        # Page limit handling
        pages_100_bool = input("Do you want to set the page limit to 100? [T/F]: \t") in {"T","True","TRUE","Y","yes","YES"}
        if pages_100_bool == True:
            self.number = 100
        else:
            self.number = 999999
        

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-son5n9"][text() = "offers with salary"]')))
        element.click()
        
        # Salary choice handling
        salary_expectations_bool = input("Do you want to provide boundaries of salary (logical alternative) [T/F]: \t") \
            in {"T","True","TRUE","Y","yes","YES"}

        if salary_expectations_bool == True:
            self.salary()

        # Localization choice handling
        self.localization_choice_bool = input("Do you want to choose location of offer?: \t") \
            in {"T","True","TRUE",'Y',"yes","YES"}
        if self.localization_choice_bool == True:
            self.location()





    def location(self):
        
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Location"]')))
        element.click()
        
        # user input
        self.choose_location = input("Please type, Which city are you interested in?: 'Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Gliwice', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Olsztyn', 'Opole', 'Poznań', 'Rzeszów', 'Szczecin', 'Toruń', 'Trójmiasto', 'Warszawa', 'Wrocław', 'Zielona Góra', 'Łódź': \t")

        if (self.choose_location in ['Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Gliwice', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Olsztyn', 'Opole', 'Poznań', 'Rzeszów', 'Szczecin', 'Toruń', 'Trójmiasto', 'Warszawa', 'Wrocław', 'Zielona Góra', 'Łódź']):
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//span[@class="MuiButton-label"][text() = "{self.choose_location}"]')))
            element.click()
        else: 
            print('There is no such location. You will have offers with all possibile cities.')
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="MuiButtonBase-root MuiIconButton-root css-tze5xj"]')))
            element.click()

    def salary(self):
        

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text() = "More filters"]')))
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
        
        # crating list of links of offers to further scraping
        links = []

        # while loop to reach destined number of pages
        while(len(links) < self.number):
            elements = self.driver.find_elements_by_css_selector("a.css-18rtd1e")
            locations = self.driver.find_elements_by_xpath("//div[@class='css-1ihx907']")

            # checking length of links before loop
            check_before = len(links)

            # for loop for elements and location
            for element, location in zip(elements, locations):
                if (self.localization_choice_bool == True and self.choose_location in ['Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Gliwice', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Olsztyn', 'Opole', 'Poznań', 'Rzeszów', 'Szczecin', 'Toruń', 'Trójmiasto', 'Warszawa', 'Wrocław', 'Zielona Góra', 'Łódź']):
                    # solving problem with displaying offers for other cities
                    if(location.text == self.choose_location):
                        link = element.get_attribute("href")
                        # if link exists in list of links - continue
                        if(link in links):
                            continue
                        else:
                            # append links
                            links.append(link)
                            # if length of links is >= predefined number of pages - break
                            if (len(links)>= self.number):
                                break
                    else:
                        break
                else:

                    link = element.get_attribute("href")
                    # if link exists in list of links - continue
                    if(link in links):
                        continue
                    else:
                        # append links
                        links.append(link)
                        # if length of links is >= predefined number of pages - break
                        if (len(links)>= self.number):
                            break

            # checking length of links after loop
            check_after = len(links)

            # press 'Page Down' key to get next list of offers
            elements[-1].send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
            
            # if length of links after loop and before loop are the same - bottom of the page - break the loop
            # if not - continue
            if check_before == check_after:
                break
            else:
                continue

        return links
    
    # Destructor
    def __del__(self):
        self.driver.quit()
        
if __name__ == '__main__':

    c = Scraper(headless_mode = True)

    links = c.offers()
    for link in links:
        print(link)
    c.__del__()
