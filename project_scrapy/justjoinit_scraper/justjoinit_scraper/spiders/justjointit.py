# -*- coding: windows-1250 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time

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
    start_urls = ["https://justjoin.it/api/offers"]
    x = input()
    print(x)

    def start_requests(self):
        yield SeleniumRequest(
            url = self.start_urls[0], 
            callback = self.parse_links,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'pre')))

    def parse_links(self, response):
        html_data = response.xpath('//pre/text()').get()
        json_data = json.loads(html_data)
        for i in json_data[0:10]:
            offers_url = "https://justjoin.it/offers/" + i["id"]
            yield SeleniumRequest(
                url = offers_url, 
                callback = self.parse_offers,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.css-1xc9aks')))

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