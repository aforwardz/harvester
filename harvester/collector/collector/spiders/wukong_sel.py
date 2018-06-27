# coding: utf-8
import re
import json
import csv
from datetime import datetime
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging


class WukongSelSpider(scrapy.Spider):
    name = 'WukongSel'
    home_url = 'https://www.wukong.com/'
    insurance = 'https://www.wukong.com/tag/6213187423061412353/'
    invest = 'https://www.wukong.com/tag/6213187420293171713/'
    fund = 'https://www.wukong.com/tag/6213187421769566721/'
    stock = 'https://www.wukong.com/tag/6213187421031369217/'
    plicai = 'https://www.wukong.com/tag/6213185666709195265/'
    licai = 'https://www.wukong.com/tag/6213187422323214849/'
    finance = 'https://www.wukong.com/tag/6213185657561418242/'
    economy = 'https://www.wukong.com/tag/6213187411782928897/'
    america = 'https://www.wukong.com/tag/6213187424823020033/'
    hongkong = 'https://www.wukong.com/tag/6347928532739426818/'
    driver = None
    faq_list = []
    count = 0
    cookie = 'ga=GA1.2.221268613.1520582867; tt_webid=6568660869164287501; tt_webid=6568660869164287501; _gid=GA1.2.1689909911.1529385541; sessionid=4b140a8d7d7b641997fb4a32d5396a50; sessionid=4b140a8d7d7b641997fb4a32d5396a50; uid_tt=0222855da1baf6cd7da7cc63a2a6ad05; uid_tt=0222855da1baf6cd7da7cc63a2a6ad05; wenda_login_status=1; wendacsrftoken=12a39c2a8f814fca485b6c6f4fe3e0ee; answer_finalFrom=; cookie_tt_page=b0d596e027031f96d348200dc62fbba1; answer_enterFrom=; _gat=1'
    headers = {
        ':authority': 'www.wukong.com',
        ':method': 'GET',
        ':path': '',
        ':scheme': 'https',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'wendacsrftoken': '12a39c2a8f814fca485b6c6f4fe3e0ee',
        'x-requested-with': 'XMLHttpRequest',
    }
    questions = []
    answers = []

    def scroll_down(self):
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(1)

    def start_requests(self):
        self.driver = webdriver.Firefox()
        print('create driver')
        self.driver.get(self.hongkong)
        try:
            # caijing = WebDriverWait(self.driver, 20).until(
            #     EC.presence_of_element_located((By.XPATH, '//a/span[text()="财经"]'))
            # )
            # caijing.click()
            # actions = ActionChains(self.driver)
            # actions.click(caijing)
            # actions.perform()

            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//div[@id="main-index-question-list"]'))
            # )
            time.sleep(3)

            for i in range(15000):  # 这里循环次数尽量大，保证加载到底
                ActionChains(self.driver).key_down(Keys.DOWN).perform()  # 相当于一直按着DOWN键
                print('已完成%d次' % i)

            time.sleep(2)
            questions = self.driver.find_elements(By.XPATH, '//div[@class="question-title"]//h2//a')
            answers = self.driver.find_elements(By.XPATH, '//div[@class="answer-item-content"]//p//a')
            self.questions = list([q.get_property("text") for q in questions])
            self.answers = list([a.get_attribute('href') for a in answers])
            print(len(self.questions), len(self.answers))
            assert len(self.questions) == len(self.answers), 'questions and answers not matched'
            # with open('wukong_insurance_faq.csv', 'w', newline='') as f:
            #     writer = csv.writer(f, dialect='excel', delimiter=',')
            #     for question, answer in zip(questions, answers):
            #         q = question.get_property("text")
            #         a = answer.get_attribute('href')
            #         print(q, a)
            #         writer.writerow([q, a])

            time.sleep(1)
        finally:
            self.driver.quit()
            for question, answer in zip(self.questions, self.answers):
                self.headers[':path'] = answer.replace(self.home_url, '')
                yield scrapy.Request(
                    url=answer,
                    headers=self.headers,
                    cookies=self.cookie,
                    callback=self.parse,
                    meta={'question': question}
                )

    def parse(self, response):
        logging.info('| Now --%s-- spider is crawling the site: %s' % (
            self.name, response.url
        ))
        first = response.xpath('(//div[@class="answer-text-full rich-text"])[1]//text()').extract()
        first = '\n'.join(first) if first else ''
        second = response.xpath('(//div[@class="answer-text-full rich-text"])[2]//text()').extract()
        second = '\n'.join(second) if second else ''
        third = response.xpath('(//div[@class="answer-text-full rich-text"])[3]//text()').extract()
        third = '\n'.join(third) if third else ''
        print(first)

        if not response.meta.get('question'):
            return
        faq = [response.meta.get('question'), first, second, third]
        self.faq_list.append(faq)

        if len(self.faq_list) >= 1000:
            with open('wukong_faq_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []

    def close(self, spider, reason):
        if len(self.faq_list):
            with open('wukong_faq_' + str(self.count) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(self.faq_list)
            self.count += 1
            self.faq_list = []

        super(WukongSelSpider, self).close('WukongSel', 'finished')
