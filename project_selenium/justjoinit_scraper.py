from selenium import webdriver
from selenium.webdriver.common.keys import Keys #selenium features for keys from keyboard
from selenium.webdriver import ActionChains #selenium features for mouse movements
from selenium.webdriver.common.by import By #selenium features By
from selenium.webdriver.support.ui import WebDriverWait #selenium features for waiting
from selenium.webdriver.support import expected_conditions as EC #selenium features for waiting
import time
import datetime
import os
from os import path
import pandas as pd
import matplotlib.pyplot as plt #plots
import logging #library for logging
import re

def clean_html(raw_html):
    """Function removing html tags from string

    Args:
        String with html code

    Returns:
        Cleaned string

    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

##################################################### Author: Michał Wrzesiński ############################################################
class Scraper():

    
    log_file_name = "logs/log_" + str(datetime.datetime.now()).replace(":","_").replace("-","_").replace(" ","_") + ".txt" #name for log file


    logging.basicConfig(
        filename=log_file_name,
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    ) # logging configuration; logs are available in logs folder

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # declaring options
    def __init__(self, headless_mode = True):
        self.headless_mode = headless_mode

        # path of geckodriver
        gecko_path = path.join(os.path.dirname(os.path.abspath('__file__')), 'geckodriver')
        url = 'https://justjoin.it/'
        options = webdriver.firefox.options.Options()
        
        # headless mode depending on the initial choice of user
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

        # Location choice handling
        self.localization_choice_bool = input("Do you want to choose location of offer?: \t") \
            in {"T","True","TRUE",'Y',"yes","YES"}
        if self.localization_choice_bool == True:
            self.location()




    # Location 
    # - if user chose location from all available - website will filter it, 
    # - if not - website close the window with cities and there will be prompt in console that: 'There is no such location. You will have offers with all possibile cities.'
    def location(self):
        
        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Location"]')))
        element.click()
        
        # user input
        self.choose_location = input("Please type, Which city are you interested in?: 'Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Gliwice', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Olsztyn', 'Opole', 'Poznań', 'Rzeszów', 'Szczecin', 'Toruń', 'Trójmiasto', 'Warszawa', 'Wrocław', 'Zielona Góra', 'Łódź': \t")

        if (self.choose_location in ['Białystok', 'Bielsko-Biała', 'Bydgoszcz', 'Częstochowa', 'Gliwice', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Olsztyn', 'Opole', 'Poznań', 'Rzeszów', 'Szczecin', 'Toruń', 'Trójmiasto', 'Warszawa', 'Wrocław', 'Zielona Góra', 'Łódź']):
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//span[@class="MuiButton-label"][text() = "{self.choose_location}"]')))
            element.click()
        else: 
            print('There is no such location. You will have offers with all possibile cities.')
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="MuiButtonBase-root MuiIconButton-root css-tze5xj"]')))
            element.click()

    # Salary
    # This part goes on ActionChains from Selenium
    # Scraper click on point on site and move to the desired position:
    # Clicking on the element finding by xpath --> move_by_offset with formula:  (11 * min_salary / 1000, 0 for minimum) and (11 * (max_salary - 50000) / 1000, 0 form maximum)
    # Multiplying by 11 and dividing by 1000 due to default settings on site (with horizontal slider)
    # for example: 0 is default minimum salary expectations: if user enter 10000 - scraper will move point from 0 to 10000 horizontally [swipe from left to right]
    # in the same way it works for maximum salary expectations -> from 50000 to exemplary 30000 [swipe from right to left]
    def salary(self):
        

        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[text() = "More filters"]')))
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

        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiButton-label"][text() = "Show offers"]')))
        element.click()

    # Offers
    # This part involves gathering links to pages
    # It is possible due to while loop (links are appended till desired number of pages or to the bottom of the website)
    # Loop for 2 lists: elements and location is necessery because of default settings of page:
    # When there are only few offers from chosen city, website displays some offers from other cities
    # Then, due to location list - we are certain that we gather links only for desired city
    # Page Down key is necessery for scrolling down - after each iteration 
        # gathering links to list
        # checking if there are no duplicates - if yes, loop ignores those links
        # checking if there new links - if no new links -> bottom of the page -> end of appending links
    def offers(self):
        
        # crating list of links of offers to further scraping
        links = []

        # while loop to reach destined number of pages
        while(len(links) < self.number):
            # lists of elements and locations before 'Page Down'
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
########################################## End of Michał Wrzesiński part ##############################################

########################################## Author: Rafał Rysiejko ####################################################
    def link_opener(self):
        
        #Call offers method to fetch url links to filtered offers.
        links = self.offers()
        
        #Create placeholders for output
        offer_link_list=[]
        offer_title_list=[]
        company_name_list=[]
        company_size_list=[]
        empoyment_type_list=[]
        experience_lvl_list=[]
        salary_list=[]
        place_list=[]
        tech_stack_list=[]
        company_page_list=[]
        direct_apply_list=[]
        offer_description_list=[]
        
        #Iterate through each offer link.
        for link in links:
            #Call driver to open a given url.
            self.driver.get(link)
            

            #Scrape appropreiate items from oppened site.
            offer_link = link
            offer_title = self.driver.find_element_by_xpath("//span[@class='css-1v15eia']").text
            company_name = self.driver.find_element_by_xpath("//a[@class='css-l4opor']").text
            company_size = self.driver.find_element_by_xpath("//div[2]/div[@class='css-1ji7bvd']").text
            empoyment_type = self.driver.find_element_by_xpath("//div[3]/div[@class='css-1ji7bvd']").text
            experience_lvl = self.driver.find_element_by_xpath("//div[4]/div[@class='css-1ji7bvd']").text
            salary = self.driver.find_element_by_xpath("//span[@class='css-8cywu8']").text
            place = self.driver.find_element_by_xpath("//div[@class='css-1d6wmgf']").text
            tech_stack = [{i.text:j.text} for i,j in zip (self.driver.find_elements_by_xpath("//div[@class='css-1eroaug']"),self.driver.find_elements_by_xpath("//div[@class='css-19mz16e']"))]
            direct_apply = True if len(self.driver.find_element_by_xpath("//button[@class='MuiButtonBase-root MuiButton-root MuiButton-text css-im43rs']").text) !=0 else False
            company_page = self.driver.find_element_by_xpath("//a[@class='css-l4opor']").get_attribute("href")
            offer_description = clean_html(self.driver.find_element_by_xpath("//div[@class='css-u2qsbz']").text)

            #Append newly scrapped elements to their corresponding lists
            offer_link_list.append(offer_link)
            offer_title_list.append(offer_title)
            company_name_list.append(company_name)
            company_size_list.append(company_size)
            empoyment_type_list.append(empoyment_type)
            experience_lvl_list.append(experience_lvl)
            salary_list.append(salary)
            place_list.append(place)
            tech_stack_list.append(tech_stack)
            company_page_list.append(company_page)
            direct_apply_list.append(direct_apply)
            offer_description_list.append(offer_description)

        #Save output to a Pandas data.frame object. 
        output = pd.DataFrame(list(zip(offer_link_list, 
                                    offer_title_list,
                                    company_name_list,
                                    company_size_list,
                                    empoyment_type_list,
                                    experience_lvl_list,
                                    salary_list,
                                    place_list,
                                    tech_stack_list,
                                    direct_apply_list,
                                    company_page_list, 
                                    offer_description_list)), columns=['offer_link', 'offer_title', 'company_name','company_size','empoyment_type','experience_lvl','salary','place','tech_stack','direct_apply','company_page','offer_description_list'])
        #Return data.frame obejct
        return output
        
    # Destructor
    def __del__(self):
        self.driver.quit()
        
if __name__ == '__main__':

    c = Scraper()
    links = c.link_opener()
    links.to_csv('output.csv', encoding='utf-8')

    c.__del__()

