# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime

from SouthCity.items import ArticalItem
nav={}

class MpageSpider(scrapy.Spider):
    name = 'mpage'
    # allowed_domains = ['http://epaper.oeeee.com/epaper/A/html/']
    start_urls = ['http://epaper.oeeee.com/epaper']

    def parse(self, response):
        html = response.body
        soup=BeautifulSoup(html,'html.parser')
        paper_div=soup.find('div','shortcutbox')
        a=paper_div.find_all('a')
        
        for i in a:
            # yield response.follow(i,callback=self.parse_section)
            href=i.get('href')
            link=response.urljoin(href)
            # link='http://epaper.oeeee.com/epaper/'+href[href.find('A'):] 
            nav[i.text]=link
            try:
                yield scrapy.Request(link,callback=self.parse_section)
            except:
                continue
        # print(nav)

    def parse_section(self, response):
        html = response.body
        soup=BeautifulSoup(html,'html.parser')
        paper_div=soup.find('div','main-list')
        a=paper_div.find_all('a')
        nav={}
        for i in a:
            href=i.get('href')
            link=response.urljoin(href)
            
            nav[i.text]=link
            try:
                yield scrapy.Request(link,callback=self.parse_page)
            except:
                continue

        # print(nav)
    def parse_page(self,response):
        # <div class="main-600 fl" id="list">
        # items = []
        detailbox=[]
        artical='  '

        html = response.body  
        soup = BeautifulSoup(html, "html.parser")  
        # 找到所有的博文代码模块  

        # try:
        info = soup.find('div', "main-600 fl")
        print(1)
        detail=info.find_all('span')
        # detailbox.append(detail[1].text)
        print(2)
        for dt in detail:
            try:
                dts=dt.text
                dts=dts[dts.find('：')+1:].strip()
                detailbox.append(dts)
            except:
                detailbox.append(dt.text)
  
        print(3)
        news=info.find('div','text')
        pp=news.find_all('p')
        print(4)
        for p in pp:
            pt = p.text
            pt = pt.strip().replace("\xa0","")
            artical += pt
        print(5)
        try:
            head1=info.find('h1').text
            head2=info.find_all('h2')
        except:
            pass
        item = ArticalItem()  
        print(6)
        item['leading_title'] = head2[0].text
        item['title'] = head1
        item['subtitle'] = head2[1].text
        item['link']=response.url
        item['writeTime']=detailbox[1]
        item['source']=detailbox[0]
        item['section']=detailbox[3]
        item['author']=detailbox[4]
        item['news']=artical
        print(7)
        # items.append(item)
        yield item
        return item
        # except:
        #     pass
        # print(item)  
