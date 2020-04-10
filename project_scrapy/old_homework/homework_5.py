# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksMusicians(scrapy.Spider):
    name = 'links_musicians'
    allowed_domains = ['https://en.wikipedia.org/']
    start_urls = ['https://en.wikipedia.org/wiki/Lists_of_musicians']

    def parse(self, response):
        xpath = "//*[@id='A']/parent::*/following-sibling::*[1]/ul/li/a/@href"
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://en.wikipedia.org' + s.get()
            yield l

class LinksMusicians_a(scrapy.Spider):
    name = 'links_musicians_a'
    allowed_domains = ['https://en.wikipedia.org/']
    try:
        with open("links_musicians.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:2]
    except:
        start_urls = []

    def parse(self, response):
        xpath = "//span[@id='Artists']/parent::*/following-sibling::*[1]/ul/li/a/@href"
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] ='https://en.wikipedia.org/' + s.get()
            yield l

class Bands(scrapy.Item):
    name = scrapy.Field()
    years = scrapy.Field()

class LinksMusicians_10(scrapy.Spider):
    name = 'links_musicians_10'
    allowed_domains = ['https://en.wikipedia.org/']
    try:
        with open("links_musicians_a.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:11]
    except:
        start_urls = []

    def parse(self, response):
        p = Bands()
        
        name_xpath        = '//h1/text()'
        years_xpath       = "//span[text()='Years active']/parent::*/following-sibling::*/text()"
        years_xpath1 = "//span[text()='Years active']/parent::*/following-sibling::*/div/ul/li/text()"
        p['name']        = response.xpath(name_xpath).getall()
        foo = response.xpath(years_xpath).getall()
        if len(foo) == 0:
            p['years']       = response.xpath(years_xpath1).getall()
        else:
            p['years']       = response.xpath(years_xpath).getall()

        yield p
   

## Excecution:
# scrapy crawl links_musicians -o links_musicians.csv
# scrapy crawl links_musicians_a -o links_musicians_a.csv
# scrapy crawl links_musicians_10 -o links_musicians_10.csv