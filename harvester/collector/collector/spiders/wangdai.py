# coding: utf-8
import re
import json
import csv
from datetime import datetime
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class WangdaiSpider(scrapy.Spider):
    name = 'p2peye.com'
    allowed_domains = ['p2peye.com']
    base_url = '/wenda/web/nativefeed/brow/'
    start_urls = [
        'https://www.p2peye.com/platform/bank/',
        # 'https://www.wukong.com/wenda/web/nativefeed/brow/?concern_id=6215497900357585410&t=1529385968230&max_behot_time=1529385571&_signature=Tb0.oRAeFpcnnXkWUhjv2E29P7'
    ]
    headers = {
        'host': 'www.p2peye.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    bank_list = []
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        print(response.status)
        plate = response.xpath('//table/tbody//tr//td[2]/a[1]/@title').extract()
        bank = '//table/tbody//tr//td[2]/a[@title="{plate}"]/../../td[5]/text()'
        for p in plate:
            xp = bank.format(plate=p)
            print(xp)
            b = response.xpath(xp).extract_first()
            print(p, b)
            if b:
                self.bank_list.append([p, b])

        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                dont_filter=True,
                headers=self.headers,
                callback=self.parse,
            )

    def close(self):
        if self.bank_list:
            with open('p2p_bank.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.bank_list)
        super(WangdaiSpider, self).close('p2peye.com', 'finished')
