# -*- coding: utf-8 -*-
import scrapy
from olx_scraper.args import info
from scrapy.http import Request
from datetime import date
from scrapy.selector import Selector
import random
from time import sleep
from scrapy.loader import ItemLoader
from olx_scraper.items import OlxScraperItem
import os
import glob
import csv
'''
----------------------------------------------------------------------------------
    FUNCTION TO CONVERT NUMBER TO MONTH
---------------------------------------------------------------------------------
'''
def num2month(num):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if num >=0 and num <=12:
        return months[num-1]
    return -1
'''
----------------------------------------------------------------------------------
    FUNCTION TO CONVERT MONTH TO NUMBER
---------------------------------------------------------------------------------
'''
def month2num(month):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if month in months:
        return (months.index(month)+1)
    return -1
'''
----------------------------------------------------------------------------------
    THIS GENERIC SPIDER SCRAPES OLX TO FIND RECENT ADS ON REQUIRED PRODUCT BY 
    THE USER
----------------------------------------------------------------------------------
'''
class ScraperSpider(scrapy.Spider):
    name = 'scrape_olx'
    start_urls = ['https://www.olx.com/']
    def __init__(self):
        self.d = date.today()
        self.min_price = 0
    def parse(self, response):
        city =info('city')
        city_new=city.replace(" ","").lower()
        product =info('product')
        product_new = product.replace(" ","-").lower()
        min_p = info('minimumprice')
        if min_p != '':
            self.min_price=int(min_p)
        url=response.url+city_new+"/"+"q-"+product_new
        yield Request(url,callback=self.parse_products)
    def parse_products(self,response):
        urls = response.xpath("//td[contains(@class,'offer')]")
        for url in urls:
            date  =url.xpath(".//*[@class='color-9 lheight14 margintop3 small']/text()").extract_first()
            abs_url=url.xpath(".//h3/a/@href").extract_first()
            title = url.xpath(".//h3/a/span/text()").extract_first()
            price = url.xpath(".//p[contains(@class,'price')]/strong/text()").extract_first().strip()
            price_split = price.replace("Rs","").strip()
            price_str=''
            if "," in price_split:
                price_split_new =price_split.split(',')
                for num in price_split_new:
                    price_str=price_str+num
            else:
                price_str =price_split
            final_price = int(price_str)
            if  final_price < self.min_price and self.min_price != 0:
                 continue
            yield Request(abs_url,callback=self.product_page,meta={"url":abs_url,"title":title,
                "priceOfProduct":price,"dateOfPost":date})    
    def product_page(self,response):
        user=response.xpath('//*[contains(@class,"userdetails")]/span/text()').extract_first()
        try:
            phone_number = response.xpath('//*[contains(@class,"contactitem")]/strong/text()').extract()[1]
        except:
            try:
                phone_number = response.xpath('//*[contains(@class,"contactitem")]/strong/text()').extract_first()
                phone_number="+92"+phone_number
            except:
                phone_number = 'Not available' 
        description=response.xpath("//*[@id='textContent']/p/text()").extract_first().strip()
        date  =response.meta.get('date')
        abs_url=response.meta.get('url')
        title = response.meta.get('title')
        price = response.meta.get('price')
        prc = response.meta.get('prc')
        
        yield{'title':title,'phone_number':phone_number,'dateOfPost':date,
        'priceOfProduct':price,'url':abs_url,'description':description,
        'user':user}


