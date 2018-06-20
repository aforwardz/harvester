# coding: utf-8
import re
import json
import csv
from datetime import datetime
import scrapy
from scrapy.exceptions import CloseSpider
from collector.utils import webpage_handler
import logging


class WukongSpider(scrapy.Spider):
    name = 'wukong.com'
    allowed_domains = ['wukong.com']
    base_url = '/wenda/web/nativefeed/brow/'
    start_urls = [
        'https://www.wukong.com/wenda/web/nativefeed/brow/',
        # 'https://www.wukong.com/wenda/web/nativefeed/brow/?concern_id=6215497900357585410&t=1529385968230&max_behot_time=1529385571&_signature=Tb0.oRAeFpcnnXkWUhjv2E29P7'
    ]
    params = {
        'concern_id': '6215497900357585410',
        't': '',
        '_signature': 'wvA5BxAemeOo0H-wpHqt8cLwOR',
        # 'max_behot_time': ''
    }
    cookie = '_ga=GA1.2.221268613.1520582867; tt_webid=6568660869164287501; wendacsrftoken=12a39c2a8f814fca485b6c6f4fe3e0ee; tt_webid=6568660869164287501; answer_finalFrom=https%3A%2F%2Fwww.google.com%2F; answer_enterFrom=; cookie_tt_page=b0d596e027031f96d348200dc62fbba1; _gid=GA1.2.1689909911.1529385541; wenda_last_concern_id=6215497900357585410'
    headers = {
        ':authority': 'www.wukong.com',
        ':method': 'GET',
        ':path': '',
        ':scheme': 'https',
        'referer': 'https://www.wukong.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'wendacsrftoken': '12a39c2a8f814fca485b6c6f4fe3e0ee',
        'x-requested-with': 'XMLHttpRequest',
    }
    behot_time = ''
    faq_list = []
    count = 0
    driver = None

    def buildQuery(self,):
        return '?' + '&'.join([key + '=' + value for key, value in self.params.items() if value])

    def start_requests(self):
        for url in self.start_urls:
            self.params['t'] = str(int(datetime.timestamp(datetime.now())))
            query = self.buildQuery()
            self.headers[':path'] = self.base_url + query
            yield scrapy.Request(
                url=url + query,
                dont_filter=True,
                headers=self.headers,
                cookies=self.cookie,
                callback=self.parse,
            )

    def parse(self, response):
        print(response.status)
        res = json.loads(response.body.decode())
        print(res)
        for index, cell in enumerate(res['data']):
            if len(self.faq_list) >= 100:
                with open('wukong_faq_' + str(self.count) + '.csv', 'w', newline='') as f:
                    writer = csv.writer(f, dialect='excel', delimiter=',')
                    writer.writerows(self.faq_list)
                self.count += 1
                self.faq_list = []

            if index == res['total_number'] - 1:
                self.behot_time = str(cell.get('behot_time'))

            q = cell['question'].get('title')
            a = cell['answer'].get('content')
            if q:
                self.faq_list.append([q, a])

        if res['has_more']:
            self.params['t'] = str(int(datetime.timestamp(datetime.now())))
            # self.params['max_behot_time'] = self.behot_time
            query = self.buildQuery()
            self.headers[':path'] = self.base_url + query
            yield scrapy.Request(
                url=self.start_urls[0] + query,
                dont_filter=True,
                headers=self.headers,
                cookies=self.cookie,
                callback=self.parse,
            )

    def close(self):
        if self.faq_list:
            with open('wukong_faq_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []
        super(WukongSpider, self).close('wukong.com', 'finished')
