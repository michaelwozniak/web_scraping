# -*- coding: utf8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_selenium import SeleniumRequest
from scrapy.utils.log import configure_logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import logging

class DataHandler(scrapy.Item):
    adress_url_offer = scrapy.Field()
    offer_title = scrapy.Field()
    company_name = scrapy.Field()
    company_size = scrapy.Field()
    empoyment_type = scrapy.Field()
    experience_lvl = scrapy.Field()
    salary = scrapy.Field()
    place = scrapy.Field()
    tech_stack = scrapy.Field()
    if_company_page_exists = scrapy.Field()
    if_direct_apply_possible = scrapy.Field()
    text_offert_description = scrapy.Field()

class OffersLinks(scrapy.Spider):
    name = 'justjoinit'
    allowed_domains = ["justjoin.it"]
    log_file_name = "logs/log_" + str(datetime.datetime.now()).replace(":","_").replace("-","_").replace(" ","_") + ".txt"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=log_file_name,
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self):
        self.start_urls = ["https://justjoin.it/api/offers"]
        print("==========================================")
        print("Please, configure scraper!")
        print("==========================================")
        pages_100_bool = input("Do you want to set the page limit to 100? [T/F]: \t") in {"T","True","TRUE","Y","yes","YES"}
        if pages_100_bool == True:
            self.pages_100 = 100
        else:
            self.pages_100 = 999999

        localization_choice_bool = input("Do you want to scrap offers from all over Poland [T]? If not, press [F].: \t") \
            in {"T","True","TRUE","yes","YES"}
        if localization_choice_bool == True:
            self.localization_choice = "ALL"
        else:
            self.localization_choice = input("Please type, Which city is interesting you: 'Berlin', 'Białystok', 'Bielsko-Biała', 'Billund', 'Bremen', 'Burbank', 'Bydgoszcz', 'Chicago', 'Chorzów', 'Culver City', 'Częstochowa', 'Dublin', 'Düsseldorf', 'Dąbrowa Górnicza', 'Gdańsk', 'Gdynia', 'Gliwice', 'Helsinki', 'Irvine', 'Katowice', 'Kielce', 'Kraków', 'Kroměříž', 'Kwidzyn', 'København', 'London', 'Londyn', 'Los Angeles', 'Los Gatos', 'Lublin', 'Lund/Stockholm', 'Luxembourgh', 'Malmo', 'Marki', 'Mediolan', 'Miami Beach', 'München', 'New York', 'Norymberga', 'Nowy Jork', 'Olsztyn', 'Opole', 'Ostrów Wielkopolski', 'Palo Alto', 'Paris', 'Pasadena', 'Portland', 'Poznań', 'Road Town', 'Rybnik', 'Rzeszów', 'Sadowa', 'San Francisco', 'Seattle', 'Singapore', 'Sopot', 'Swarzędz', 'Szczecin', 'Tczew', 'Toruń', 'Tychy', 'Unterföhring', 'Ustroń', 'Valetta', 'Warsaw', 'Warszawa', 'Wałbrzych', 'Wrocław', 'Zabierzów', 'Zielona Góra', 'Łódź', 'Świdnica', 'Краків': \t")
            if self.localization_choice not in {'Berlin', 'Berlin ', 'Białystok', 'Bielsko-Biała', 'Billund', 'Bremen', 'Burbank', 'Bydgoszcz', 'Chicago', 'Chorzów', 'Culver City', 'Częstochowa', 'Dublin', 'Düsseldorf', 'Dąbrowa Górnicza', 'Gdańsk', 'Gdynia', 'Gliwice', 'Helsinki', 'Irvine', 'Katowice', 'Kielce', 'Kraków', 'Kroměříž', 'Kwidzyn', 'København', 'London', 'Londyn', 'Los Angeles', 'Los Gatos', 'Lublin', 'Lund/Stockholm', 'Luxembourgh', 'Malmo', 'Marki', 'Mediolan', 'Miami Beach', 'München', 'New York', 'Norymberga', 'Nowy Jork', 'Olsztyn', 'Opole', 'Ostrów Wielkopolski', 'Palo Alto', 'Paris', 'Pasadena', 'Portland', 'Poznań', 'Road Town', 'Rybnik', 'Rzeszów', 'Sadowa', 'San Francisco', 'Seattle', 'Singapore', 'Sopot', 'Swarzędz', 'Szczecin', 'Tczew', 'Toruń', 'Tychy', 'Unterföhring', 'Ustroń', 'Valetta', 'Warsaw', 'Warszawa', 'Wałbrzych', 'Wrocław', 'Zabierzów', 'Zielona Góra', 'Łódź', 'Świdnica', 'Краків'}:
                self.localization_choice = "ALL"
                print("Wrong localization, scaper localization set to all cities!")

        salary_expectations_bool = input("Do you want to provide boundaries of salary (logical alternative) [T/F]: \t") \
            in {"T","True","TRUE","yes","YES"}
        if salary_expectations_bool == True:
            self.salary_expectations_lower = int(input("Please provide lower boundaries:: \t"))
            self.salary_expectations_upper = int(input("Please provide upper boundaries: \t"))
        
        if (salary_expectations_bool == False) or \
                (isinstance(self.salary_expectations_lower, (int, float, complex)) and not isinstance(self.salary_expectations_lower, bool) == False) or \
                (isinstance(self.salary_expectations_upper, (int, float, complex)) and not isinstance(self.salary_expectations_upper, bool) == False):
            self.salary_expectations_lower = 0
            self.salary_expectations_upper = 1000000

    def start_requests(self):
        yield SeleniumRequest(
            url = self.start_urls[0], 
            callback = self.parse_links,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'pre')))

    def parse_links(self, response):
        html_data = response.xpath('//pre/text()').get()
        json_data = json.loads(html_data)
        pages_100_handler = 0
        
        for i in json_data:
            if type(i["salary_from"]) != type(None) and type(i["salary_to"]) != type(None):
                if self.localization_choice == "ALL":
                    if (self.salary_expectations_lower <= int(i["salary_from"]) and int(i["salary_from"])<=self.salary_expectations_upper) or (self.salary_expectations_upper >= int(i["salary_to"]) and int(i["salary_to"]) >=self.salary_expectations_lower) or (i["salary_to"]>self.salary_expectations_upper and (i["salary_from"]<self.salary_expectations_lower)):
                        if pages_100_handler < self.pages_100:
                            offers_url = "https://justjoin.it/offers/" + i["id"]
                            pages_100_handler += 1
                            yield SeleniumRequest(
                                url = offers_url, 
                                callback = self.parse_offers,
                                wait_time=10,
                                wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.css-1xc9aks')))
                        else:
                            break
                else: 
                    if self.localization_choice == i["city"]:
                        if (self.salary_expectations_lower <= int(i["salary_from"]) and int(i["salary_from"])<=self.salary_expectations_upper) or (self.salary_expectations_upper >= int(i["salary_to"]) and int(i["salary_to"]) >=self.salary_expectations_lower) or (i["salary_to"]>self.salary_expectations_upper and (i["salary_from"]<self.salary_expectations_lower)):
                            if pages_100_handler < self.pages_100:
                                offers_url = "https://justjoin.it/offers/" + i["id"]
                                pages_100_handler += 1
                                yield SeleniumRequest(
                                    url = offers_url, 
                                    callback = self.parse_offers,
                                    wait_time=10,
                                    wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.css-1xc9aks')))
                            else:
                                break

    def parse_offers(self, response):
        handler = DataHandler()
        handler["offer_title"] = response.xpath("//span[@class='css-1v15eia']/text()").get()
        handler["company_name"] = response.xpath("//a[@class='css-l4opor']/text()").get()
        handler["company_size"] = response.xpath("//div[2]/div[@class='css-1ji7bvd' and 2]/text()").get()
        handler["empoyment_type"] = response.xpath("//div[3]/div[@class='css-1ji7bvd' and 2]/text()").get()
        handler["experience_lvl"] =  response.xpath("//div[4]/div[@class='css-1ji7bvd' and 2]/text()").get()
        handler["salary"] = response.xpath("//span[@class='css-8cywu8']/text()").get()
        handler["place"] = response.xpath("//div[@class='css-1d6wmgf']/text()").get()
        handler["tech_stack"] = [{i:j} for i,j in zip (response.xpath("//div[@class='css-1eroaug']/text()").getall() , 
                response.xpath("//div[@class='css-19mz16e']/text()").getall())]
        handler["if_company_page_exists"] = True if len(response.xpath("//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineHover css-66z1rr MuiTypography-colorPrimary']")) != 0 else False
        handler["if_direct_apply_possible"] = True if len(response.xpath("//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained css-j75g8 MuiButton-containedPrimary']/span[@class='MuiButton-label' and 1]")) != 0 else False
        handler["text_offert_description"] = response.xpath("//div[@class='css-gz8dae']/div/span").get()
        handler["adress_url_offer"] = response.request.url

        yield handler
