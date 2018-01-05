# coding: utf-8
import jieba
import thulac
from string import punctuation
all_punctuation = punctuation + """～！￥…×（）【】、—《》？“”："""


def cut_to_sentences_and_tokenize(paragraph):
    thu = thulac.thulac(seg_only=True)
    end_punc = '.?!。！？'
    ret = []
    sentence = ''
    max_length = 0
    for item in paragraph:
        sentence += item
        if item in end_punc:
            tokenize = thu.cut(sentence, text=True).split(' ')
            max_length = max((max_length, len(tokenize)))
            ret.append(tokenize)
            sentence = ''
    # 还需考虑句子中没有这些标点符号的case
    if sentence:
        tokenize = thu.cut(sentence, text=True).split(' ')
        max_length = max((max_length, len(tokenize)))
        ret.append(tokenize)
    index = 0
    # 去除只包含标点符号的行
    while index < len(ret):
        _list = ret[index]
        if len(_list) == 1 and _list[0] in end_punc:
            ret.pop(index)
        else:
            index += 1

    return max_length, ret
