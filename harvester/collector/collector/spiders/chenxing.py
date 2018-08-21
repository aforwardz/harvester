# coding: utf-8
import re
import json
import csv
import time
from datetime import datetime
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.exceptions import CloseSpider
import logging


class ChenXingSpider(scrapy.Spider):
    name = 'morningstar.com'
    allowed_domains = ['morningstar.com']
    base_url = '/wenda/web/nativefeed/brow/'
    home = 'http://cn.morningstar.com/fundselect/default.aspx'
    headers = {
        'host': 'cn.morningstar.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    driver = None
    code, fund, three_rate, five_rate = [], [], [], []
    count = 0

    def go_next(self):
        print('go to next page')
        next_page = self.driver.find_elements(By.XPATH, '//div[@id="cphMain_AspNetPager1"]//a')[-2]
        if next_page.get_attribute('disabled') == 'true':
            return False
        time.sleep(1)
        next_page.click()
        return True

    def parse_page(self):
        try:
            items = self.driver.find_elements(By.XPATH, '//table[@id="cphMain_gridResult"]//tr')
            for index, item in enumerate(items):
                if index == 0:
                    continue
                tds = item.find_elements_by_tag_name('td')
                self.code.append(tds[1].find_element_by_tag_name('a').get_property('text'))
                self.fund.append(tds[2].find_element_by_tag_name('a').get_property('text'))
                three = tds[4].find_element_by_tag_name('img').get_attribute('src')
                five = tds[5].find_element_by_tag_name('img').get_attribute('src')
                self.three_rate.append(three.split('/')[-1][0])
                self.five_rate.append(five.split('/')[-1][0])
            print(self.code, self.three_rate, self.five_rate)
            assert len(self.code) == len(self.three_rate) == len(self.five_rate), \
                'code and three_rate and five_rate not matched'

            time.sleep(1)
        except:
            pass

    def start_requests(self):
        self.driver = webdriver.Chrome()
        print('create driver')
        self.driver.get(self.home)
        time.sleep(3)
        # self.driver.execute_script("window.stop")

        self.parse_page()
        while self.go_next():
            self.parse_page()

        self.handle_data()

    def handle_data(self):
        with open('chenxing.csv', 'w') as f:
            writer = csv.writer(f, dialect='excel', delimiter=',')
            writer.writerows(zip(self.code, self.fund, self.three_rate, self.five_rate))

    def close(self, spider, reason):
        if len(self.faq_list):
            with open('wukong_faq_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []

        super(ChenXingSpider, self).close('morningstar.com', 'finished')
