# coding: utf-8
import re


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


def strip_space(string):
    sentence_list = string.split('\n')
    for index, sentence in enumerate(sentence_list):
        sentence_list[index] = sentence.strip(' \t')

    return '\n'.join(sentence_list)


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
