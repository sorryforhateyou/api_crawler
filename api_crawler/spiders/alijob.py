# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from pprint import pprint
import json
import scrapy
from api_crawler.items import ApiCrawlerItem


class AlijobSpider(scrapy.Spider):
    name = 'alijob'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['https://job.alibaba.com/zhaopin/socialPositionList/doList.json']
    headers = {
        'Origin': 'https://job.alibaba.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://job.alibaba.com/zhaopin/positionList.htm',
        'Authority': 'job.alibaba.com',
    }
    # form data
    # pageSize=10&t=0.9778208747231463&keyWord=&location=%E5%8C%97%E4%BA%AC&second=&first=&pageIndex=1
    meta_data = {
        'pageSize' : '10',
        't' : '0.9778208747231463',
        'keyWord' : '',
        'location' : '%E5%8C%97%E4%BA%AC&',
        'second' : '',
        'first' : '',
        'pageIndex' : '1',
    }


    def parse(self, response):
        for index in range(1):
            i = index + 1
            headers = self.headers
            print(headers)
            url = self.start_urls[0]
            self.log('alijob_url: %s, %d' %(url, i))
            ## 将得到的页面地址传送给单个页面处理函数进行处理 -> parse_content()
            meta_data = self.meta_data
            meta_data['pageIndex'] = '%d'%i
            yield scrapy.Request(url, callback=self.parse_content, headers=headers, meta=meta_data)


    def parse_content(self, response):
        '''将得到的单个作品的页进行分析取值'''
        self.log('alijob_detail_url: %s' % response.url)
        r = response.body_as_unicode()
        # item = ApiCrawlerItem()
        r = json.loads(r)
        print(type(r))
        #returnValue
        #exceptionDesc
        #isSuccess
        if r['isSuccess'] == False:
            self.log('alijob_request_error: %s' % r['exceptionDesc'])
            return
        else:
            self.log('alijob_request_success: %s' % r['exceptionDesc'])
        job_info = r['returnValue']
        #pageIndex
        #pageSize
        #startPosForMysql
        #totalRecord
        #datas
        #totalPage
        #endPos
        #startPos
        self.log('alijob_request_result: pageIndex: %d, pageSize: %d, startPosForMysql: %d, totalRecord: %d, totalPage: %d, startPos: %d, endPos: %d'%(
                job_info['pageIndex'], 
                job_info['pageSize'], 
                job_info['startPosForMysql'], 
                job_info['totalRecord'], 
                job_info['totalPage'], 
                job_info['startPos'], 
                job_info['endPos'], 
            ))
        job_data = job_info['datas']
        '''
        description <class 'str'>
        name <class 'str'>
        id <class 'int'>
        status <class 'str'>
        applyed <class 'bool'>
        favorited <class 'bool'>
        code <class 'str'>
        requirement <class 'str'>
        gmtModified <class 'int'>
        degree <class 'str'>
        gmtCreate <class 'int'>
        departmentName <class 'str'>
        workLocation <class 'str'>
        workExperience <class 'str'>
        expired <class 'bool'>
        isUrgent <class 'str'>
        isOpen <class 'str'>
        departmentId <class 'int'>
        firstCategory <class 'str'>
        secondCategory <class 'str'>
        effectiveDate <class 'int'>
        uneffectualDate <class 'int'>
        recruitNumber <class 'int'>
        isNew <class 'str'>
        '''
        alijob_item = ApiCrawlerItem()
        alijob_item['jobs'] = job_data
        return alijob_item


