# -*- coding: utf-8 -*-

#ALIEXPRESS BANEA EN CERO COMA, SOLO PROBAR CUANDO SEPA LO QUE ESTOY HACIENDO

from scrapy.spiders import Spider 
import scrapy
import selenium
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy import Request
import requests
import urllib.request
from datetime import date
import os


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


class AliexpressSpider(scrapy.Spider):
    name = 'aliexpress'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/category/204000221/t-shirts.html?trafficChannel=main&catName=t-shirts&CatId=204000221&ltype=wholesale&SortType=default&page=1']

    
    weborigin = 'Aliexpress.com'
    date_found = date.today()
    User = 'None'
    
    
    def parse_document(self, url):

        fields = dict()
        fields['weborigin'] = self.weborigin
        fields['date'] = self.date_found
        fields ['producturl'] = ''
        fields ['User'] = 'store-name'
        
        document = Document()
        self.driver.get(url)

        for key, name in fields.items():
            try:
                element = self.driver.find_element_by_class_name(name)
                document.setField(key, element.text)
            except:
                document.setField(key, None)

        return document


    def __init__(self, *arg, **kwarg):
        
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.max_pages = 5

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("-–disable-web-security")
        options.add_argument("--no-sandbox")

        capabilities = options.to_capabilities()
        self.driver = webdriver.Chrome('/home/mgarcia/Documentos/master_big_data/capitulo_5/ejercicio_3/tools/chromedriver', desired_capabilities=capabilities)



    def parse(self, response):
        
        #item = TeeChipItem()
        #img_urls = []
        suffix = '/front/medium.jpg'
        list_urls = []
        
        
        for page in range(1, 5):
            print ("------------------------------------------ PÁGINA "+ str(page) +" ------------------------------------------")
            #time.sleep(5)
            self.driver.get('https://www.aliexpress.com/category/204000221/t-shirts.html?trafficChannel=main&catName=t-shirts&CatId=204000221&ltype=wholesale&SortType=default&page='+str(page))

            images = self.driver.find_elements_by_tag_name('img')
            for image in images:
                src = image.get_attribute('src')
                image_url = image.get_attribute('src')
                
                #if image_url.endswith(suffix):
                list_urls.append(image_url)
                    
        #print ("================================================================================================================================================")            
        #print ("=========================================================== FIN DEL SCRAP ======================================================================")
        #print ("================================================================================================================================================")    
  
        #para borrar duplicados
        list_urls = list(set(list_urls))

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        myPath = '/home/mgarcia/Documentos/TeeRipper/imagenes/Aliexpress/'

        i=1

        with open("url_images.txt", "w") as text_file:
            for url in list_urls:
                filename = 'imagen_' + str(i)
                fullfilename = os.path.join(myPath, filename)
                urllib.request.urlretrieve(url, fullfilename)
                i = i+ 1
                text_file.write(url+'\n')
        
        self.driver.close()
