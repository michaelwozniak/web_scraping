# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json


class Link(scrapy.Item):
    links = scrapy.Field()

class OffersLinks(scrapy.Spider):
    name = 'offers_links'
    allowed_domains = ["justjoin.it"]
    start_urls = ["https://justjoin.it/api/offers"]

    def start_requests(self):
        yield SeleniumRequest(
            url = "https://justjoin.it/api/offers", 
            callback = self.parse_results,
            wait_time=10)

    def parse_results(self, response):
        html_data = response.xpath('//pre/text()').get()
        json_data = json.loads(html_data)
        for i in json_data:
            l = Link()
            l['links'] = i
            yield l
