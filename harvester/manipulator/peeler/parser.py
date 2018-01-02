# coding: utf-8
import json
import lxml.etree

from functools import reduce

import logging

logger = logging.getLogger('parser')


class BaseParser(object):
    """
    Call parse to parse a html file
    ``get_content`` ``init`` ``get_value_from_selector`` are
    implemented by Sub-Parser
    """
    def __init__(self):
        self.source = ''
        self.source_file = ''

    @staticmethod
    def _get_source(content, file_path=''):
        source, source_file = content.get('url', ''), file_path
        return source, source_file

    def get_content(self, file):
        """
        从传入的file中获取内容
        :param file: 文件
        :return: 内容
        """
        pass

    def init(self, file_path):
        """
        """
        pass

    def get_value_from_selector(self, selector, raw=False):
        """
        根据content和selector获取对应的值
        :param content:
        :param selector:
        :return: value
        """
        pass

    def parse(self, selectors):
        """
        :type selectors: QuerySet
        :return: data list
        """
        data_list = list()
        for selector_obj in selectors:
            try:
                selector = selector_obj.selector
                if not selector:
                    continue
                value = self.get_value_from_selector(selector, raw=True)
            except:
                continue
            else:
                if value:
                    data_list.append(
                        (selector_obj.attr_name, value, selector_obj.attr)
                    )
        return data_list


class HtmlParser(BaseParser):

    def get_content(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            try:
                return json.loads(content)
            except ValueError:
                return content


class HtmlXPathParser(HtmlParser):

    def __init__(self):
        super(HtmlXPathParser, self).__init__()
        self.tree = None

    def _init_etree(self, content):
        html = content.get('html')
        assert bool(html) is True, 'html 为空'
        self.tree = lxml.etree.HTML(html.lower())

    def init(self, file_path):
        """
        :param file_path: file path
        """
        content = self.get_content(file_path)
        self.source, self.source_file = self._get_source(content, file_path)
        self._init_etree(content)

    def get_value_from_selector(self, selector, raw=False):
        """
        传入 selector 解析该选择器对应的 value
        :param selector: attr selector
        :return:
        """
        sel = self._replace(selector.lower())
        selection = self.tree.xpath(sel)
        if selection:
            if len(selection) > 1:
                text = '\n'.join([s.xpath('string(.)') for s in self.tree.xpath(sel)])
            else:
                text = self.tree.xpath(sel)[0].xpath('string(.)')
        else:
            text = self.tree.xpath(self._elimin_table(sel))[0].xpath('string(.)')

        return text.strip()

    @staticmethod
    def _elimin_table(xpath):
        """
        返回一个不带tbody标签的xpath
        :param xpath: 带tbody标签
        :return: 不带tbody标签
        """
        try:
            return xpath.replace('tbody/', '', 1)
        except:
            return xpath

    @staticmethod
    def _replace(xpath):
        tags = (
            ('/text', ''),
        )
        return reduce(lambda s, tag: s.replace(*tag), tags, xpath)
