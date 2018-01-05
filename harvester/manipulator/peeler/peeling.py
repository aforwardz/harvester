# coding: utf-8
import os
from datetime import datetime
from django.conf import settings
from django.utils.html import strip_tags
from peeler.parser import HtmlXPathParser
from seed.models import Seed
from peeler.tools import cut_to_sentences_and_tokenize
from utils import utilities
import logging

logger = logging.getLogger('peeler')


class Peeler(object):
    def __init__(self, selector):
        self.peeler = HtmlXPathParser()
        self.selector = selector

    def strip_special_extra(self, content, extra):
        return content.replace(extra, '')

    def clean_content(self, content):
        """
        1. 清除html
        2. 多个space合并为一个
        3. 全角字符改为半角
        4. 清除微信表情
        """
        content = self.strip_special_extra(content, '【更多英超资讯】')
        handles = [
            strip_tags,
            utilities.strQ2B,
            utilities.strip_sticker,
            utilities.merge_spaces,
            utilities.merge_newlines,
            utilities.strip_space,
            utilities.replace_special
        ]

        for handle in handles:
            content = handle(content)

        return content.strip()

    def start(self, host, date=''):
        if not date:
            date = str(datetime.now().date())
        page_root = os.path.abspath(os.path.join(
            settings.BASE_DIR, os.pardir, 'collector/pages'))
        page_path = os.path.join(page_root, host, date)
        for root, _, files in os.walk(page_path):
            logger.info(('%d files To Be Parsed In: %s/%s/' % (
                len(files), host, date)))
            peeler = self.peeler
            for i, f in enumerate(files):
                logger.info(('| %d/%d | %s | Parsing: %s' % (
                    i + 1, len(files), host, f)))
                fp = os.path.join(root, f)
                if not os.path.isfile(fp):
                    continue
                peeler.init(fp)
                content = peeler.get_value_from_selector(self.selector)
                clean_content = self.clean_content(content)
                print(clean_content)
                paragraphs = list(filter(lambda x: len(x) > 0, clean_content.split('\n')))
                word_3_list = list(map(utilities.cut_paragraph_to_sentences, paragraphs))
                seed = Seed(
                    source=peeler.source,
                    content=content,
                    clean_content=clean_content,
                    content_type=1,
                    words={'word': word_3_list}
                )
                seed.save()
