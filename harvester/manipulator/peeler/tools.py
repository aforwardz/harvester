# coding: utf-8
import jieba
import thulac
from string import punctuation
all_punctuation = punctuation + """～！￥…×（）【】、—《》？“”："""
end_punc = '.?!。！？'
thu = thulac.thulac(seg_only=True)


def cut_to_sentences_and_tokenize(paragraph):
    ret = []
    sentence = ''
    for item in paragraph:
        sentence += item
        if item in end_punc:
            ret.append(thu.cut(sentence, text=True).strip().split(' '))
            sentence = ''
    # 还需考虑句子中没有这些标点符号的case
    if sentence:
        ret.append(thu.cut(sentence, text=True).strip().split(' '))
    index = 0
    # 去除只包含标点符号的行
    while index < len(ret):
        _list = ret[index]
        if len(_list) == 1 and _list[0] in end_punc:
            ret.pop(index)
        else:
            index += 1

    return ret
