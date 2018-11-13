# coding: utf-8
import re
import json
import copy
import random
import hashlib
import datetime
import functools
import itertools
import jieba
import jieba.posseg

from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags


ZH_NUMBER_MAP = {
    '零': 0, '一': 1, '七': 7, '三': 3, '九': 9, '二': 2, '五': 5,
    '八': 8, '六': 6, '四': 4, '十': 10, '伍': 5, '叁': 3, '壹': 1,
    '拾': 10, '捌': 8, '柒': 7, '玖': 9, '肆': 4, '贰': 2, '陆': 6,
    '两': 2,
}

ZH_NUMERAL_MAP = {
    '十': 1e1, '百': 1e2, '千': 1e3, '万': 1e4, '亿': 1e8,
}


def is_han(text):
    '''
    判断text是否为汉字
    '''
    return all('\u4e00' <= char <= '\u9fff' for char in text)


def is_number(char):
    """判断一个unicode是否是数字
    """
    return char.isdigit() or char in ZH_NUMBER_MAP


def is_alpha(char):
    """判断一个unicode是否是英文字母
    """
    return ('\u0041' <= char <= '\u005a') \
           or ('\u0061' <= char <= '\u007a')


def is_alnum(char):
    """判断一个unicode是否是字母或者数字
    """
    return is_number(char) or is_alpha(char)


def is_unit(char):
    """判断是否为单位
    """
    units = {'年', '月', '日', '天', '万', '千', '个', '号', '期', '类'}
    return char in units


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code in {12288, 160}:  # 12288: 全角空格 160: 'NO-BREAK SPACE'
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strip_sticker(string):
    """去除表情符号, 如：
    [微笑][闭嘴][惊讶]...
    """
    return re.sub(r'\[[\u4e00-\u9fffa-zA-Z]{1,3}\]', '', string)


def merge_newlines(string):
    return re.sub('\n+( +\n)*', '\n', string)


def merge_spaces(string, merge2=' '):
    """ Merge several spaces to 'merge2' """
    return re.sub(' +', merge2, string)


def strip_newline(string):
    return re.sub('\n', '', string)


def strip_space(string):
    sentence_list = string.split('\n')
    for index, sentence in enumerate(sentence_list):
        sentence_list[index] = sentence.strip(' \t')

    return '\n'.join(sentence_list)


def strip_nonword(string, rep=''):
    """ 去除非 word 干扰符号"""
    string = re.sub(r'\W+', rep, string)
    return string


def replace_special(string, rep='~'):
    """空格 / - 连接数字时需要特殊处理。
    如： 12 + 6 2亿  ltp 分词会分成 12 + 62 亿
        100~299-7.0% 分词会分成 100 ~ 299-7.0 %
    囧"""
    # 12 2亿
    string = re.sub(r'(\d+) (\d+)', '\\1%s\\2' % rep, string)
    # -100
    string = re.sub(r'-(\d+|[a-zA-Z]+)', '%s\\1' % rep, string)
    # /1
    string = re.sub(r'/(\d+|[a-zA-Z]+)', '%s\\1' % rep, string)
    # 万7 %
    string = re.sub(r'万(\d+|[a-zA-Z]+)', '万%s\\1' % rep, string)
    # 100w/W
    string = re.sub(r'(\d+)[wW]', '\\1万', string)
    return string


def cut_paragraph_to_sentences(paragraph):
    end_punc = '.?!。！？'
    ret = []
    sentence = ''
    for item in paragraph:
        sentence += item
        if item in end_punc:
            ret.append(sentence)
            sentence = ''
    # 还需考虑句子中没有这些标点符号的case
    if sentence:
        ret.append(sentence)
    index = 0
    # 去除只包含标点符号的行
    while index < len(ret):
        _list = ret[index]
        if len(_list) == 1 and _list[0] in end_punc:
            ret.pop(index)
        else:
            index += 1

    return ret


def get_name_chars(string):
    name_chars = list(strip_nonword(
        string.replace(' ', '')).strip().upper())
    return name_chars


def get_name_cut(string):
    """把中文串拆成字，英文/数字拆成整体，
    并且去除无关紧要的符号
    :type string: str
    TODO: Test Similarity Search 的精度问题
    """
    s_cleaned = strip_nonword(string.replace(' ', '')).strip()
    s_len = len(s_cleaned)
    name_cut = ''
    for i, char in zip(itertools.count(), s_cleaned):
        char = char.upper() if is_alpha(char) else char
        if i < s_len - 1 and is_alnum(char):
            if is_alnum(s_cleaned[i + 1]) or is_unit(s_cleaned[i + 1]):
                name_cut += char
            else:
                name_cut += char + ' '
        elif char == ' ' or i == s_len - 1:
            name_cut += char
        else:
            name_cut += char + ' '

    return re.sub(' +', ' ', name_cut)


def gen_hash(string):
    hash_md5 = hashlib.md5()
    hash_md5.update(string.encode())
    hash_code = hash_md5.hexdigest()
    return hash_code


def clean_content(content):
    """ Clean 的逻辑会影响到预测
    1. 清除html
    2. 多个space合并为一个
    3. 全角字符改为半角
    4. 清除微信表情
    """
    handles = [
        strip_tags,
        strQ2B,
        strip_sticker,
        merge_spaces,
        merge_newlines,
        strip_space,
        strip_newline,
        replace_special
    ]

    for handle in handles:
        content = handle(content)

    return content.strip()


def constructURLParams(fields):
    if fields:
        params = '?'
        for key,value in fields.items():
            if isinstance(value,list):
                if len(value):
                    if params != '?':
                        params += '&'
                    params += key + '=' + ','.join(value)
            else:
                if value:
                    if params != '?':
                        params += '&'
                    params += key + '=' + str(value)
        return params
    else:
        return ''


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def lazy_property(func):
    '''
    Decorators that stores the result in a member named after the decorated function (prepended with a prefix) and returns this value on any subsequent calls.
    '''
    attribute = '_cache_' + func.__name__
    @property
    @functools.wraps(func)
    def decorator(self):
        if not hasattr(self,attribute):
            setattr(self,attribute, func(self))
        return getattr(self,attribute)

    return decorator


def define_scope(func):
    import tensorflow as tf

    attribute = '_cache_' + func.__name__

    @property
    @functools.wraps(func)
    def decorator(self):
        if not hasattr(self, attribute):
            with tf.name_scope(func.__name):
                setattr(self, attribute, func(self))
        return getattr(self, attribute)

    return decorator


def eliminate_bracket(s):
    """
    :param s: list
    :return:
    """
    bracket = ['(', ')', '[', ']', '{', '}']
    s = list(filter(lambda x: x not in bracket, s))
    return s