# coding: utf-8
import re
import scrapy
from scrapy.exceptions import CloseSpider
from collector.utils import webpage_handler
import logging


class TZuQiuSpider(scrapy.Spider):
    name = 'tzuqiu.cc'
    allowed_domains = ['tzuqiu.cc']
    base_url = 'http://app.gooooal.com/newslist.do?dictid={id}'
    start_urls = [
        'http://www.tzuqiu.cc/',
    ]
    page = 1
    webpage_path = webpage_handler.create_dir(name)
    link_sel = '//ul[@class="newsList"]//a/@href'
    main_sel = ['//div[@class="news_main"]']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.league_parse,
            )

    def league_parse(self, response):
        print(response.status)

        link_list = response.xpath('//div[@id="competition-league-list"]//a/@href').extract()
        nation_list = response.xpath('//div[@id="competition-league-list"]//a/img/@alt').extract()
        name_list = response.xpath('//div[@id="competition-league-list"]//a/text()').extract()
        assert len(link_list) == len(nation_list) == len(name_list), 'First Length Not Matched'
        for link, nation, name in zip(link_list, nation_list, name_list):
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.team_parse,
                meta={'nation': nation, 'name': name}
            )

    def team_parse(self, response):

        link_list = response.xpath('//div[@id="rankTable0_wrapper"]//td[2]/a/@href').extract()
        name_list = response.xpath('//div[@id="rankTable0_wrapper"]//td[2]/a/@title').extract()
        assert len(link_list) == len(name_list), 'Second Length Not Matched'
        for link, name in zip(link_list, name_list):
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.player_parse,
                meta={'league_nation': response.meta.get('nation'),
                      'league_name': response.meta.get('name'),
                      'team_name': name,
                      }
            )

    def player_parse(self, response):
        link_list = response.xpath('//div[@id="playersTable_wrapper"]//tr[@class="odd"|"even"]/td[2]/a/@href').extract()
        for link in link_list:
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.parse,
                meta={'league_nation': response.meta.get('league_nation'),
                      'league_name': response.meta.get('league_name'),
                      'team_name': response.meta.get('team_name'),
                      }
            )

    def parse(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        webpage_handler.save_webpage(response, self.webpage_path,
                                     selectors=self.main_sel)

