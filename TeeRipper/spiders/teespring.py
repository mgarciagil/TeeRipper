# -*- coding: utf-8 -*-
import scrapy
import selenium
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy import Request

class Page():
    def parse(self, response):
        print(response.url)
        self.driver.get(response.url)


class Document(object):

    def __init__(self):
        self.document = dict()
        self.document['weborigin'] = ''
        self.document['date'] = ''
        self.document['producturl'] = ''
        self.document['User'] = ''

    def setDescription(self, text):
        self.document['weborigin'] = text
    
    def setPrize(self, date):
        self.document['date'] = date

    def setYear(self, value):
        self.document['producturl'] = text

    def setYear(self, value):
        self.document['User'] = text
    
    def setField(self, field, value):
        self.document[field] = value



class TeespringSpider(scrapy.Spider):
    name = 'teespring'
    allowed_domains = ['teespring.com']
    start_urls = ['http://teespring.com/']

    def parse(self, response):
        pass
