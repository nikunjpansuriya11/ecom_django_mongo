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
from webdriver_manager.chrome import ChromeDriverManager

from ecom_api.models import Product, ScrapeProductUrl, Sizes, Images
from ecom_api.serializers.product_serializer import AllProductSerializer


# This management command is for product desciption scrape from links and add in database
class Command(BaseCommand):
    
    def handle(self, *args, **options):

        all_product_url = Product.objects.filter(desc_add=False)
        print(all_product_url)


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

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


        for product_url in all_product_url:


            driver.get(product_url.product_url)
            driver.maximize_window()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            req = driver.page_source 
            driver.quit()
            soup_c = BeautifulSoup(req, "html.parser")

            productsdesc_outerboxes_tag = soup_c.find('section', class_="tw-f1zr7x")
            print(productsdesc_outerboxes_tag)
            productsdesc_outerbox_tag = productsdesc_outerboxes_tag.find('div', class_="grid gap-8 lg:gap-10 grid-cols-1 md:grid-cols-2")
            print(productsdesc_outerbox_tag)
            productsdesc_allboxs_tag = productsdesc_outerbox_tag.findChildren("div" , recursive=False)
            desc_list = []
            for productsdesc_box_tag in productsdesc_allboxs_tag:
                desc_details_list = []
                print("-------------------productsdesc_box_tag--------------------")
                print(productsdesc_box_tag)
                desc_title_tag = productsdesc_box_tag.find('h3')
                desc_title = desc_title_tag.text

                desc_details_tag = productsdesc_box_tag.find('p')
                if desc_details_tag is not None:
                    desc_details = desc_details_tag.text
                    desc_details_list.append(desc_details)

                desc_details_tag = productsdesc_box_tag.find_all('li')
                if len(desc_details_tag) > 0:
                    for desc_detail_tag in desc_details_tag:
                        desc_detail = desc_detail_tag.text
                        desc_details_list.append(desc_detail)

                desc_details_tag = productsdesc_box_tag.find_all('span')
                if len(desc_details_tag) > 0:
                    for desc_detail_tag in desc_details_tag:
                        desc_detail = desc_detail_tag.text
                        desc_details_list.append(desc_detail)

                desc_details_tag = productsdesc_box_tag.find('div')
                if desc_details_tag is not None:
                    desc_details = desc_details_tag.text
                    desc_details_list.append(desc_details)

                desc_dir = {
                    "title":desc_title,
                    "desc":desc_details_list,
                }
                desc_list.append(desc_dir)

            product_url.desc = desc_list
            product_url.desc_add = True
            product_url.save()

        driver.quit()