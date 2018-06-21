# coding: utf-8
import re
import csv
import json
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class ZaihangSpider(scrapy.Spider):
    name = 'zaih.com'
    allowed_domains = ['zaih.com']
    account_url = 'https://fd.zaih.com/api/v1/tags/38/accounts?page={acc_page}&per_page=20'
    content_url = 'https://fd.zaih.com/feed_api/v1/accounts/{account_id}/activities?page={act_page}&per_page=20&order_by=score'
    start_urls = []
    acc_page, act_page = 2, 1
    acc_header = {
        'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22163c89bf89b242-001c13d3ba2d21-3b720b58-2073600-163c89bf89cafb%22%2C%22%24device_id%22%3A%22163c89bf89b242-001c13d3ba2d21-3b720b58-2073600-163c89bf89cafb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwx2.qq.com%2F%3F%26lang%3Dzh_CN%22%2C%22%24latest_referrer_host%22%3A%22wx2.qq.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; fduid=U79CaGyL27Jzo6c1; _ga=GA1.2.766555961.1528079055; _gid=GA1.2.948087866.1528079055; _smt_uid=5b14a2cf.2cc2d4c0; zg_did=%7B%22did%22%3A%20%22163c89c3bac4d5-095adfe9ccbed-3b720b58-1fa400-163c89c3badd49%22%7D; zg_aa3e7dc3269a48b4b0fb9d035761074f=%7B%22sid%22%3A%201528079072.176%2C%22updated%22%3A%201528079209.019%2C%22info%22%3A%201528079072178%7D',
        'Host': 'fd.zaih.com',
        'Pragma': 'no-cache',
        'Referer': 'https://fd.zaih.com/category/38?from=mentor_category&from_order=39',
        'sa-browser': 'Chrome',
        'sa-from': 'https://fd.zaih.com/categories',
        'sa-os': 'web',
        'sa-platform': 'PC',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'X-NewRelic-ID': 'VQUDVFFTDxACUFFbAgYOXg=='
    }
    cont_header = {

    }
    question_list = []
    result_page = 23

    def start_requests(self):
        for i in range(1, self.acc_page):
            yield scrapy.Request(
                url=self.account_url.format(acc_page=i),
                dont_filter=True,
                callback=self.parse,
                headers = self.acc_header,
                meta={'page': i}
            )

    def parse(self, response):
        print(response.status)
        res = json.loads(response.body.decode())
        if res:
            with open('accounts_' + str(response.meta.get('page')) + '.txt', 'w') as f:
                f.write(str(res))
        for acc in res[:2]:
            acc_id = acc.get('id')
            nickname = acc.get('nickname')
            print(nickname)
            answers_count = acc.get('answers_count')
            all_page = answers_count // 20 + 1
            for p in range(1, all_page + 1):
                if acc_id:
                    yield scrapy.Request(
                        url=self.content_url.format(account_id=acc_id, act_page=p),
                        dont_filter = True,
                        callback = self.parse_question,
                        headers = self.acc_header,
                        meta={'nickname': nickname}
                    )



    def parse_question(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        res = json.loads(response.body.decode())
        for queston in res:
            if len(self.question_list) >= 200:
                with open('question_list_' + str(self.result_page) + '.csv', 'w', newline='') as f:
                    print(self.question_list)
                    writer = csv.writer(f, dialect='excel', delimiter=',')
                    writer.writerows(self.question_list)
                self.result_page += 1
                self.question_list = []
            self.question_list.append((response.meta.get('nickname'), queston.get('content')))

    def close(self):
        if self.question_list:
            with open('question_list_' + str(self.result_page) + '.csv', 'w', newline='') as f:
                print(self.question_list)
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.question_list)
            self.result_page += 1
            self.question_list = []
        super(ZaihangSpider, self).close('zaih.com', 'finished')