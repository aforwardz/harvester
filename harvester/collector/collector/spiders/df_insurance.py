# coding: utf-8
import re
import csv
import json
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class DFInsuranceSpider(scrapy.Spider):
    name = 'eastmoney.com'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://data.eastmoney.com/money/insurance.html']
    header = {
        'Cookie': 'st_pvi=47022187680818; st_si=00945221312124',
        'Host': 'data.eastmoney.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.google.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }
    insurance_list = []
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse,
                headers = self.header,
            )

    def parse(self, response):
        print(response.status)
        sel_list = response.xpath('//tbody//tr')
        for i in range(1, len(sel_list) + 1):
            name = response.xpath('//tbody//tr[position()=' + str(i) + ']//td[@class="name"]/a/@title').extract_first()
            print(name)
            if name:
                # info = response.xpath('//tbody//tr[position()=' + str(i) + ']//td[position()<10]/text()').extract()
                self.insurance_list.append((name, 40))

        if len(self.insurance_list) > 400:
            i_l = self.insurance_list
            self.insurance_list = []
            with open('insurance_list_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(i_l)
            self.count += 1

        next = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next:
            yield scrapy.Request(
                url=response.urljoin(next),
                dont_filter=True,
                callback=self.parse,
            )

    def close(self):
        if self.insurance_list:
            with open('insurance_list_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.insurance_list)
            self.count += 1
            self.question_list = []
        super(DFInsuranceSpider, self).close('eastmoney.com', 'finished')
