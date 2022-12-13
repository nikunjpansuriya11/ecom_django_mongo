from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests 
import re
from urllib.request import urlopen 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import unittest
import pandas as pd
import urllib.parse
import undetected_chromedriver as uc 
import math      
from ecom_api.models import Product, ScrapeProductUrl, Sizes, Images
from ecom_api.serializers.product_serializer import AllProductSerializer
from webdriver_manager.chrome import ChromeDriverManager


# This management command is for product link scrape and add in database
class Command(BaseCommand):

    def handle(self, *args, **options):
        options = webdriver.ChromeOptions()

        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("disable-infobars")
        options.add_argument('--no-proxy-server')
        options.add_argument('--disable-gpu')
        options.add_argument('log-level=3')
        options.add_argument('--no-sandbox')
        options.add_argument('--autoplay-policy=no-user-gesture-required')
        options.add_argument('--start-maximized')    
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--enable-popup-blocking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", [
            "enable-logging",
            "enable-automation",
            "ignore-certificate-errors",
            "safebrowsing-disable-download-protection",
            "safebrowsing-disable-auto-update",
            "disable-client-side-phishing-detection"])
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        prefs = {"credentials_enable_service": True,
                "profile.password_manager_enabled": True}
        options.add_experimental_option("prefs", prefs)

        all_url_list = [{
            "type":"new arrivels",
            'url':'https://in.puma.com/in/en/new-arrivals'
        },{
            "type":"womens",
            'url':'https://in.puma.com/in/en/womens'
        },{
            "type":"mens",
            'url':'https://in.puma.com/in/en/mens'
        },{
            "type":"kids",
            'url':'https://in.puma.com/in/en/kids'
        },{
            "type":"sport",
            'url':'https://in.puma.com/in/en/collections'
        },{
            "type":"outlet",
            'url':'https://in.puma.com/in/en/outlet/shop-all-outlet'
        }]

        new_url_list = []
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        for i in all_url_list:
            url = i['url']
            type = i['type']
            driver.get(url)
            driver.maximize_window()
            elements = driver.find_elements(By.CLASS_NAME, "tw-1dfrg5w")
            for ele in elements:
                if ele.text == "Product Type":
                    ele.click()


            req = driver.page_source 
            soup = BeautifulSoup(req, "html.parser")
            page_get = soup.find_all('li', class_="a-disabled")
            all_cat_list = []
            all_cat = soup.find_all('span', class_="text-puma-black text-base")
            for i in all_cat:
                all_cat_list.append(i.text)

            new_data = {
                "type": type,
                "url": url,
                "all_cat":all_cat_list
            }

            new_url_list.append(new_data)


        driver.quit()
        for i in new_url_list:
            url = i['url']
            type = i['type']
            all_cat = i['all_cat']

            for j in all_cat:
                product_page_url = url+ "?pref_deptCode=" + urllib.parse.quote_plus(j)
                req = requests.get(product_page_url)
                soup_a = BeautifulSoup(req.text, "html.parser")

                all_data_number = soup_a.find('span', class_="uppercase font-bold text-lg md:text-xl")
                numbertext_of_product = all_data_number.text

                number_of_product = int(re.findall("\d+", numbertext_of_product)[0])
                if number_of_product > 24:
                    offset_number = math.floor(number_of_product/24)
                    new_url = product_page_url + "&offset=" + str(offset_number*24)
                    req_a = requests.get(new_url)
                    soup_b = BeautifulSoup(req_a.text, "html.parser")
                else:
                    soup_b = soup_a

                page_get = soup_b.find_all('a', class_="tw-hqslau tw-xbcb1y flex overflow-x-scroll scroll-snap")

                for i in page_get:
                    product_url = "https://in.puma.com" + str(i.get('href'))
                    if not ScrapeProductUrl.objects.filter(product_url=product_url).exists():
                        ScrapeProductUrl.objects.create(product_url=product_url, product_type=type)


