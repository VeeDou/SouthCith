# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# </pre><pre name="code" class="python">
#encoding:utf8  
"""
补充SQL语句
补充建表语句

展示网页模板
简历项目、从mysql输出到网页
"""

import pymysql
import logging
from hashlib import md5
import datetime

 
class MySQLStoreCnblogsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='TESTDB',
            user='pymysql',
            passwd='123123',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        global NewTable_Tag

        # linkmd5id = self._get_linkmd5id(item)
        now = datetime.datetime.now()
        date=str(now.date())
        date_s=date[:4]+date[5:7]+date[8:]
        print(date_s)
        sql='CREATE TABLE SC_%s (leading_title varchar(255), title varchar(255), subtitle varchar(255), link varchar(2000) NOT NULL, writeTime datetime, source varchar(255),section varchar(255),author varchar(255),news text,updated datetime)'%date_s

        sql_query = "SELECT 1 from SC_%s where link = '%s'"%(date_s,item['link'])
        
        sql_update = """UPDATE sc_%s set leading_title = '%s' ,
                                         title = '%s', 
                                         subtitle = '%s' ,
                                         link = '%s' , 
                                         writetime = '%s' , 
                                         source = '%s' ,
                                         section = '%s' , 
                                         author = '%s' ,
                                         news = '%s' ,
                                         updated = '%s' 
                                    where link = '%s'
                    """% (date_s,
                          item['leading_title'],
                          item['title'],
                          item['subtitle'],
                          item['link'],
                          item['writeTime'],
                          item['source'],
                          item['section'],
                          item['author'],
                          item['news'],
                          now,
                          item['link'])


        sql_insert =  """
                    insert into sc_%s(leading_title, title, subtitle, link, writeTime,source,section,author,news,updated) 
                    values('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')
                    """% (date_s,
                        item['leading_title'],
                        item['title'],
                        item['subtitle'],
                        item['link'],
                        item['writeTime'],
                        item['source'],
                        item['section'],
                        item['author'],
                        item['news'],
                        now)
        print('我在loc1')


        #tag 如何不重复检查
        self.cursor.execute('show tables')
        tables=self.cursor.fetchall()
        if ('sc_20170811',) not in all_t:
            try:
                self.cursor.execute(sql)
            except Exception as e:
                # raise e
                pass
        print('我在loc2') 

        try:
            self.cursor.execute(sql_query)
            ret = self.cursor.fetchone()
            if ret:
                self.cursor.execute(sql_update)
                print("成功更新一条数据!")
                #print """
                #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
                #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
            else:
                self.cursor.execute(sql_insert)
                print("成功插入一条数据!")
                #print """
                #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
                #    values(%s, %s, %s, %s, %s, %s)
                #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
            print('我在loc3')
            self.connect.commit()
            
            # self.cursor.close() # 关闭连接

        except Exception as error:
            logging.warning(error)
        return item

    # def _get_linkmd5id(self, item):
    #     #url进行md5处理，为避免重复采集设计
    #     return md5(item['link']).hexdigest()

