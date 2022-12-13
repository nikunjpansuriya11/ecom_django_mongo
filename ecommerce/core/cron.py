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

def product_link_scrapper():

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
    driver = uc.Chrome()

    for i in all_url_list:
        url = i['url']
        type = i['type']
        print(type)
        driver.get(url)
        driver.maximize_window()
        elements = driver.find_elements(By.CLASS_NAME, "tw-1dfrg5w")
        print(elements)
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


    print(new_url_list)

    driver.quit()
    # all_urls_of_products = []
    for i in new_url_list:
        url = i['url']
        type = i['type']
        all_cat = i['all_cat']

        for j in all_cat:
            product_page_url = url+ "?pref_deptCode=" + urllib.parse.quote_plus(j)
            print(product_page_url)  

            req = requests.get(product_page_url)
            soup_a = BeautifulSoup(req.text, "html.parser")

            # print(len(all_cat_list))
            all_data_number = soup_a.find('span', class_="uppercase font-bold text-lg md:text-xl")
            numbertext_of_product = all_data_number.text
            print(all_data_number.text)

            number_of_product = int(re.findall("\d+", numbertext_of_product)[0])
            if number_of_product > 24:
                offset_number = math.floor(number_of_product/24)
                print("||||||||||",offset_number*24)

                print("--->",number_of_product)

                new_url = product_page_url + "&offset=" + str(offset_number*24)
                print(new_url)
                req_a = requests.get(new_url)
                soup_b = BeautifulSoup(req_a.text, "html.parser")
            else:
                soup_b = soup_a

            page_get = soup_b.find_all('a', class_="tw-hqslau tw-xbcb1y flex overflow-x-scroll scroll-snap")

            print(len(page_get))
            for i in page_get:
                product_url = "https://in.puma.com" + str(i.get('href'))
                if not ScrapeProductUrl.objects.filter(product_url=product_url).exists():
                    ScrapeProductUrl.objects.create(product_url=product_url, product_type=type)
                # all_urls_of_products.append(product_url)
                # print(i.get('href'))



    # print(all_urls_of_products) 


def product_data_scrapper():

    all_product_url = ScrapeProductUrl.objects.filter(is_scraped=False)

    for product_url in all_product_url:
        req = requests.get(product_url.product_url)
        soup_c = BeautifulSoup(req.text, "html.parser")

        # print(len(all_cat_list))
        productname_text_tag = soup_c.find('h1', id="pdp-product-title")
        productname_text = str(productname_text_tag.text)
        print(productname_text)

        product_price_tag = soup_c.find('span', class_="whitespace-nowrap text-base font-bold override:md:text-2xl override:opacity-100")
        if product_price_tag is not None:
            product_price = product_price_tag.text

            product_price = float("".join(re.findall("\d+", product_price)))
            print(product_price)
            product_orgprice= 0

        else:
            product_price_tag = soup_c.find('span', class_="whitespace-nowrap text-base text-puma-red font-bold override:text-xl override:md:text-2xl")
            product_price = product_price_tag.text
            product_price = float("".join(re.findall("\d+", product_price)))
            print(product_price)
            product_orgprice_tag = soup_c.find('span', class_="whitespace-nowrap text-base line-through opacity-50 override:font-bold override:opacity-100")
            product_orgprice = product_orgprice_tag.text
            product_orgprice = float("".join(re.findall("\d+", product_orgprice)))
            
            print(product_orgprice)


        productcolor_text_outertag = soup_c.find('div', class_="flex flex-col space-y-1.5")
        productcolor_text_tag = productcolor_text_outertag.find('h2', class_="text-sm")
        productcolor_text = productcolor_text_tag.text
        print(productcolor_text)

        size_list = []
        productsizes_text_outertag = soup_c.find_all('span', class_="absolute inset-0 flex items-center justify-center")
        for productsize_text_outertag in productsizes_text_outertag:
            productsize_text_tag = productsize_text_outertag.find('span', class_="text-sm")
            productsize_text = productsize_text_tag.text
            size_list.append({"shoes_size":productsize_text})
        print(size_list)


        url_list = []
        productsimages_url_tag = soup_c.find_all('img', class_="w-full bg-puma-black-800 aspect-1-1")
        for productsimage_url_tag in productsimages_url_tag:
            productsimage_url = str(productsimage_url_tag.get('src'))
            url_list.append({"image_url":productsimage_url})
        print(url_list)

        if not Product.objects.filter(product_url=product_url.product_url).exists():
            pr_url = str(product_url.product_url)
            pr_type = str(product_url.product_type)
            Product.objects.create(product_url = pr_url, type = pr_type, name = productname_text, price = product_price, dis_price = product_orgprice, color = productcolor_text, size = size_list, images = url_list, desc={})



def product_desc_scrapper():

    all_product_url = Product.objects.filter(desc_add=False)
    print(all_product_url)

    driver = uc.Chrome()
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