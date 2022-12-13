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

# This management command is for product data scrape from links and add in database
class Command(BaseCommand):

    def handle(self, *args, **options):

        all_product_url = ScrapeProductUrl.objects.filter(is_scraped=False)

        for product_url in all_product_url:
            req = requests.get(product_url.product_url)
            soup_c = BeautifulSoup(req.text, "html.parser")

            productname_text_tag = soup_c.find('h1', id="pdp-product-title")
            productname_text = str(productname_text_tag.text)

            product_price_tag = soup_c.find('span', class_="whitespace-nowrap text-base font-bold override:md:text-2xl override:opacity-100")
            if product_price_tag is not None:
                product_price = product_price_tag.text

                product_price = float("".join(re.findall("\d+", product_price)))
                product_orgprice= 0

            else:
                product_price_tag = soup_c.find('span', class_="whitespace-nowrap text-base text-puma-red font-bold override:text-xl override:md:text-2xl")
                product_price = product_price_tag.text
                product_price = float("".join(re.findall("\d+", product_price)))
                product_orgprice_tag = soup_c.find('span', class_="whitespace-nowrap text-base line-through opacity-50 override:font-bold override:opacity-100")
                product_orgprice = product_orgprice_tag.text
                product_orgprice = float("".join(re.findall("\d+", product_orgprice)))
                


            productcolor_text_outertag = soup_c.find('div', class_="flex flex-col space-y-1.5")
            productcolor_text_tag = productcolor_text_outertag.find('h2', class_="text-sm")
            productcolor_text = productcolor_text_tag.text

            size_list = []
            productsizes_text_outertag = soup_c.find_all('span', class_="absolute inset-0 flex items-center justify-center")
            for productsize_text_outertag in productsizes_text_outertag:
                productsize_text_tag = productsize_text_outertag.find('span', class_="text-sm")
                productsize_text = productsize_text_tag.text
                size_list.append({"shoes_size":productsize_text})


            url_list = []
            productsimages_url_tag = soup_c.find_all('img', class_="w-full bg-puma-black-800 aspect-1-1")
            for productsimage_url_tag in productsimages_url_tag:
                productsimage_url = str(productsimage_url_tag.get('src'))
                url_list.append({"image_url":productsimage_url})

            if not Product.objects.filter(product_url=product_url.product_url).exists():
                pr_url = str(product_url.product_url)
                pr_type = str(product_url.product_type)
                Product.objects.create(product_url = pr_url, type = pr_type, name = productname_text, price = product_price, dis_price = product_orgprice, color = productcolor_text, size = size_list, images = url_list, desc={})

