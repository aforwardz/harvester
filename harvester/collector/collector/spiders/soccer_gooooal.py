# coding: utf-8
import re
import scrapy
from scrapy.exceptions import CloseSpider
from collector.utils import webpage_handler
import logging


class GooooalSpider(scrapy.Spider):
    name = 'gooooal.com'
    allowed_domains = ['gooooal.com']
    base_url = 'http://app.gooooal.com/newslist.do?dictid={id}'
    start_urls = [
        # 'A001',
        'A002',
        'A007',
        'A0040201',
        'A00302'
    ]
    news_list_url = 'http://app.gooooal.com/newslist.do?dictid={id}&pageNo={page}&totalCount='
    news_url = 'http://news.gooooal.com/{nids}/{nid}.html'
    page = 1
    webpage_path = webpage_handler.create_dir(name)
    link_sel = '//ul[@class="newsList"]//a/@href'
    main_sel = ['//div[@class="news_main"]']

    def start_requests(self):
        for did in self.start_urls:
            yield scrapy.Request(
                url=self.base_url.format(id=did),
                dont_filter=True,
                callback=self.parse,
                meta={did: did}
            )

    def parse(self, response):
        print(response.status)
        pattern = re.compile('\d.*(?=\))')

        link_list = response.xpath(self.link_sel).extract()
        if not link_list:
            raise CloseSpider('END')
        for link in link_list:
            if pattern.findall(link):
                newsId = pattern.findall(link)[0]
                yield scrapy.Request(
                    url=self.news_url.format(
                        nids=newsId[:6],
                        nid=newsId
                    ),
                    dont_filter=True,
                    callback=self.parse_news
                )

        self.page += 1
        yield scrapy.Request(
            url=self.news_list_url.format(id=response.meta.get('did'), page=self.page),
            dont_filter=True,
            callback=self.parse
        )

    def parse_news(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        webpage_handler.save_webpage(response, self.webpage_path,
                                     selectors=self.main_sel)
