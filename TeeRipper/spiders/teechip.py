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
from selenium.common.exceptions import NoSuchElementException
import sys
from os import path
import datetime


def get_product_code_product(url):
    product_code = url.split('ProductCode=')[1]
    return product_code

def get_product_code_image(url):
    product_code = url.split('/')[8]
    return product_code


class TeechipSpider(scrapy.Spider):
    
    product = dict()
    product['product_code'] = ''
    product['web_origin'] = 'teechip.com'
    product['date'] = datetime.date.today()
    product['product_url'] = ''
    product['user'] = 'None'

    name = 'teechip'
    allowed_domains = ['milanuncios.com']
    start_urls = ['https://teechip.com/shop/women/t-shirts/filtered/page/1']
    
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
        
        suffix = '/front/medium.jpg'
        readed_images = []
        readed_urls = []
        page = 25
        
        hay_siguiente = True
        
        while hay_siguiente is True:

            url = self.driver.get('https://teechip.com/shop/women/t-shirts/filtered/page/'+str(page))

            images_urls = self.driver.find_elements_by_tag_name('img')
            
            elems = self.driver.find_elements_by_css_selector(".RetailProductList a.d-ib[href]")
            product_urls = [elem.get_attribute('href') for elem in elems]

            for image in images_urls:
                src = image.get_attribute('src')
                image_url = image.get_attribute('src')
                
                if image_url.endswith(suffix):
                    readed_images.append(image_url)
                           
            page = page + 1

            try:
                self.driver.find_element_by_css_selector('a.d-ib.py-p75.w-3.ta-center.color-black .mdi-chevron-right')

            except NoSuchElementException:
                hay_siguiente = False


        #print ("================================================================================================================================================")            
        #print ("=========================================================== FIN DEL SCRAP ======================================================================")
        #print ("================================================================================================================================================")    
  

        #para borrar duplicados
        images_urls = list(set(images_urls))
        product_urls = list(set(product_urls))

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        myPath = '/home/mgarcia/Documentos/TeeRipper/imagenes/'

        i=1

        #guardamos las url en archivos de texto temporalmente
        with open("url_images.txt", "w") as text_file:
            for image in images_urls:
                print(str(image))
                print(len(str(image)))
                #filename = get_product_code_image(str(image))
                filename = 'imagen_' + str(i)
                fullfilename = os.path.join(myPath, filename)
                urllib.request.urlretrieve(image, fullfilename)
                i = i+ 1
                text_file.write(image+'\n')


        with open("url_products.txt", "w") as text_file:
            for product in product_urls:
                text_file.write(product+'\n')


        self.driver.close()

