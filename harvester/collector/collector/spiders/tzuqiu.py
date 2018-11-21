# coding: utf-8
import re
import scrapy
from scrapy.exceptions import CloseSpider
from collector.utils import webpage_handler
import logging


class TZuQiuSpider(scrapy.Spider):
    name = 'tzuqiu.cc'
    allowed_domains = ['tzuqiu.cc']
    start_urls = [
        'http://www.tzuqiu.cc/',
    ]
    main_sel = ['//div[@class="player-info"]']
    headers = {
        'Cookie': 'announceId=20180103001; _ga=GA1.2.1154887626.1542713850; _gid=GA1.2.678285143.1542713850; Hm_lvt_b83b828716a7230e966a4555be5f6151=1542713849,1542771411; JSESSIONID=D51224D3FB06159A2ACD431E41A0B67C; Hm_lpvt_b83b828716a7230e966a4555be5f6151=1542771845',
        'Host': 'www.tzuqiu.cc',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }

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
        headers = self.headers
        headers['Referer'] = 'http://www.tzuqiu.cc/'
        for link, nation, name in zip(link_list, nation_list, name_list):
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.team_parse,
                headers=self.headers,
                meta={'nation': nation, 'name': name}
            )

    def team_parse(self, response):
        # con = response.xpath('//table[@id="rankTable0"]//a[contains(@href, "teams")]').extract()
        # print(con)
        link_list = response.xpath('//table[@id="rankTable0"]//a[contains(@href, "teams")]/@href').extract()
        name_list = response.xpath('//table[@id="rankTable0"]//a[contains(@href, "teams")]/@title').extract()
        print(name_list, link_list)
        assert len(link_list) == len(name_list), 'Second Length Not Matched'
        headers = self.headers
        headers['Referer'] = response.url
        for link, name in zip(link_list, name_list):
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.player_parse,
                headers=headers,
                meta={'league_nation': response.meta.get('nation'),
                      'league_name': response.meta.get('name'),
                      'team_name': name,
                      }
            )

    def player_parse(self, response):
        link_list = response.xpath('//table[@id="playersTable"]//a[contains(@href, "players")]/@href').extract()
        name_list = response.xpath('//table[@id="playersTable"]//a[contains(@href, "players")]/@title').extract()
        print('Players: ', name_list)
        headers = self.headers
        headers['Referer'] = response.url
        for link, name in zip(link_list, name_list):
            yield scrapy.Request(
                url=response.urljoin(link),
                dont_filter=True,
                callback=self.parse,
                headers=headers,
                meta={'league_nation': response.meta.get('league_nation'),
                      'league_name': response.meta.get('league_name'),
                      'team_name': response.meta.get('team_name'),
                      'name': name,
                      }
            )

    def parse(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        league_nation = response.meta.get('league_nation')
        league_name = response.meta.get('league_name')
        team_name = response.meta.get('team_name')
        name = response.meta.get('name')

        webpage_path = webpage_handler.create_dir(self.name, suffix='/'.join([league_nation, league_name, team_name]))
        webpage_handler.save_webpage(response, webpage_path,
                                     selectors=self.main_sel,
                                     page_name=name)

