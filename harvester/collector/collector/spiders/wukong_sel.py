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


class WukongSelSpider(object):
    def __init__(self):
        self.home_url = 'https://www.wukong.com/'
        self.driver = None
        self.answer_dict = {}

    def scroll_down(self):
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(1)

    def start(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.home_url)
        try:
            caijing = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a/span[text()="财经"]'))
            )
            caijing.click()
            # actions = ActionChains(self.driver)
            # actions.click(caijing)
            # actions.perform()

            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//div[@id="main-index-question-list"]'))
            # )
            time.sleep(3)

            for i in range(25000):  # 这里循环次数尽量大，保证加载到底
                ActionChains(self.driver).key_down(Keys.DOWN).perform()  # 相当于一直按着DOWN键
                print('已完成%d次' % i)

            time.sleep(2)
            questions = self.driver.find_elements(By.XPATH, '//div[@class="question-title"]//h2//a')
            answers = self.driver.find_elements(By.XPATH, '//div[@class="answer-item-content"]//p//a')
            print(len(questions), len(answers))
            assert len(questions) == len(answers), 'questions and answers not matched'
            with open('wukong_faq.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                for question, answer in zip(questions, answers):
                    q = question.get_property("text")
                    a = answer.get_attribute('href')
                    print(q, a)
                    writer.writerow([q, a])

            time.sleep(1)
        finally:
            self.driver.quit()

    def crawl_answsers(self):
        with open('wukong_faq.csv', 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            for line in reader:
                q = line[0]
                link = line[1]
                yield scrapy.Request(
                    url=link,
                    dont_filter=True,
                    callback=self.parse,
                    meta={'question': q}
                )

    def parse(self, response):
        answers = response.xpath('//div[@class="answer-text-full rich-text"]')


if __name__ == '__main__':
    wk = WukongSelSpider()
    wk.start()
