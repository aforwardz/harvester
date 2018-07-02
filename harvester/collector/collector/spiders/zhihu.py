# coding: utf-8
import re
import csv
import json
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu.com'
    allowed_domains = ['zhihu.com']
    question_base = 'https://www.zhihu.com/question/{id}'
    start_urls = [
        'https://www.zhihu.com/api/v4/topics/19555939/feeds/top_question?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.content%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.comment_count&offset=0&limit=50'
    ]
    header = {
        ':authority': 'www.zhihu.com',
        ':method': 'GET',
        ':path': '',
        ':scheme': 'https',
        # 'referer': 'https://wx2.qq.com/?&lang=zh_CN',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }
    faq_list = []
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            self.header[':path'] = url.replace('https://www.zhihu.com', '')
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse,
                headers=self.header,
            )

    def parse(self, response):
        print(response.status)
        res = json.loads(response.body.decode())

        if res and res['data']:
            for question in res['data']:
                self.header[':path'] = '/question/' + str(question['target']['id'])
                yield scrapy.Request(
                    url=self.question_base.format(id=question['target']['id']),
                    callback=self.parse_answer,
                    headers=self.header,
                    meta={'id': question['target']['id'], 'title': question['target']['title']}
                )

        if res['paging'] and res['paging']['next']:
            next_page = res['paging']['next']
            self.header[':path'] = next_page.replace('https://www.zhihu.com', '')
            yield scrapy.Request(
                url=next_page,
                dont_filter=True,
                callback=self.parse,
                headers=self.header,
            )

    def parse_answer(self, response):
        q_id = response.meta.get('id')
        q_title = response.meta.get('title')
        a1 = response.xpath('(//div[@class="RichContent-inner"])[1]//text()').extract()
        a2 = response.xpath('(//div[@class="RichContent-inner"])[2]//text()').extract()
        print(q_id, q_title, ''.join(a1) if a1 else '', ''.join(a2) if a2 else '')
        if len(self.faq_list) >= 1000:
            with open('zhihu_faq_list_' + str(self.count) + '.csv', 'w', newline='') as f:
                print(self.faq_list)
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []
        self.faq_list.append([q_id, q_title, ''.join(a1) if a1 else '', ''.join(a2) if a2 else ''])

    def close(self):
        if self.faq_list:
            with open('zhihu_faq_list_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []
        super(ZhihuSpider, self).close('zhihu.com', 'finished')
