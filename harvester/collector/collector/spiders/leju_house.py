# coding: utf-8
import re
import csv
import json
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class LejuSpider(scrapy.Spider):
    name = 'leju.com'
    allowed_domains = ['leju.com']
    start_urls = ['http://house.leju.com/']
    header = {
        'Cookie': 'M_CITY=sh; gatheruuid=5b21d34dde37e954; refer_domain=google.com; s2=1528945238925_WADLON; co=1623551438925_CN53ZB; imclientToken=303918996_0_471a6a4bc9768b836cfd9bc399baf71b_910f34bc33024c5284c58b40f1feb525_; relationCache_303918996=%7B%7D; cy_ec_id=7bdddc7592de8307551ba9363b1de73c',
        'Host': 'house.leju.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.google.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }
    house_list = []
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
        district_urls = response.xpath("//div[@class='l_ovh']//dl//dt//a/@href").extract()
        assert district_urls, 'no district urls'
        for url in district_urls:
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse_district,
            )


    def parse_district(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        house = response.xpath("//div[@class='b_titBox']//h2//a/text()").extract()
        if house and type(house) == list:
            self.house_list.extend(house)
            if len(self.house_list) > 400:
                h_l = self.house_list
                self.house_list = []
                with open('house_list_' + str(self.count) + '.csv', 'w', newline='') as f:
                    writer = csv.writer(f, dialect='excel', delimiter=',')
                    writer.writerows(zip(h_l, [80] * len(h_l)))
                self.count += 1

        next = response.xpath("//a[@class='next']/@href").extract_first()
        if next:
            yield scrapy.Request(
                url=next,
                dont_filter=True,
                callback=self.parse_district,
            )
