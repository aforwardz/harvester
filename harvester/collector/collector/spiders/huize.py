# coding: utf-8
import re
import csv
import json
import scrapy
from scrapy.exceptions import CloseSpider
import logging


class HuizeSpider(scrapy.Spider):
    name = 'huize.com'
    allowed_domains = ['huize.com']
    start_urls = ['https://www.huize.com/brand/list/']
    home_header = {
        ':authority': 'www.huize.com',
        ':method': 'GET',
        ':path': '/brand/list/',
        ':scheme': 'https',
        'cookie': 'acw_tc=7ae44a8615368297937907325e023f38b55e62310839a651d4ef04dc0a; _ga=GA1.2.375179403.1536829795; Hm_lvt_27ca7fb7008b01737e4fc53e00aa3b35=1536829794,1536889662; UtmCookieKey={"UtmSource":"","UtmMedium":"","UtmTerm":"","UtmContent":"","UtmCampaign":"","UtmUrl":"https%3a%2f%2fwww.huize.com%2fbrand%2flist%2f","UtmSE":"","Keywords":""}; Hm_lpvt_27ca7fb7008b01737e4fc53e00aa3b35=1536895232; hz_guest_key=19qrI3HPjHZ21AixzyYV_1536829794629_3_0_0; hz_visit_key=1BP0g3hr5HZ3HKggi1y8_1536895232746_2_1536895232746; hz_view_key=19qrI3HPjHZ21AixzyYV3ozaIyoiIHZ1Sy4j7ccE_1536895232746_https%253A%252F%252Fwww.huize.com%252Fbrand%252Fdetail%252F17; _gat=1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }
    detail_header = {
        ':authority': 'www.huize.com',
        ':method': 'GET',
        ':path': '',
        ':scheme': 'https',
        'referer': 'referer: https://www.huize.com/brand/list/',
        'cookie': 'acw_tc=7ae44a8615368297937907325e023f38b55e62310839a651d4ef04dc0a; _ga=GA1.2.375179403.1536829795; Hm_lvt_27ca7fb7008b01737e4fc53e00aa3b35=1536829794,1536889662; hz_guest_key=19qrI3HPjHZ21AixzyYV_1536829794629_2_0_0; Hm_lpvt_27ca7fb7008b01737e4fc53e00aa3b35=1536889664; UtmCookieKey={"UtmSource":"","UtmMedium":"","UtmTerm":"","UtmContent":"","UtmCampaign":"","UtmUrl":"https%3a%2f%2fwww.huize.com%2fbrand%2flist%2f","UtmSE":"","Keywords":""}',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }
    company_list = []
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse,
                headers=self.home_header,
            )

    def parse(self, response):
        print(response.status)
        brand_urls = response.xpath("//li[@class='brand-item']//a/@href").extract()
        for url in brand_urls:
            self.detail_header[':path'] = url
            yield scrapy.Request(
                url=response.urljoin(url),
                dont_filter=True,
                headers=self.detail_header,
                callback=self.parse_com,
            )

    def parse_com(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        logo = response.xpath("//div[@class='bgfw mt15 pt15 pb15']//span[@class='mr10']/img/@src").extract_first()
        name = response.xpath("//div[@class='bgfw mt15 pt15 pb15']//span[@class='mr10']/img/@alt").extract_first()
        intro = response.xpath("//div[@class='bor-top pt15 mt20 pl30 pr30 f14 lh20 fc6']//p/text()").extract()
        tel = response.xpath("//div[@class='bor-top pl30 pr30 pt15 f14 mt20 ']//span/text()").extract_first()

        self.company_list.append([name, logo, intro, tel])

    def close(self, spider, reason):
        with open('huize_insurance_ins.csv', 'w') as f:
            writer = csv.writer(f, dialect='excel', delimiter=',')
            writer.writerows(self.company_list)
        super(HuizeSpider, self).close('huize.com', 'finished')
