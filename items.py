# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticalItem(scrapy.Item):
    leading_title = scrapy.Field() #大标题  
    title = scrapy.Field() 
    subtitle = scrapy.Field() #副标题
    link = scrapy.Field() #链接  
    source = scrapy.Field()
    writeTime = scrapy.Field() #编写时间  
    section = scrapy.Field() #板块  
    author = scrapy.Field() #作者
    news =  scrapy.Field()  #新闻内容
