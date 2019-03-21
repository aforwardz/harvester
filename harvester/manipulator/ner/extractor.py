from processor.preprocess import fin_cut


class FinNewsEventExtractor(object):
    def __init__(self):
        pass

    def cut_words(self, sentence):
        return fin_cut(sentence)


fnee = FinNewsEventExtractor()


if __name__ == '__main__':
    sentence = '金瑞矿业跨界恐遭叫停，重组标的业绩未达标已停牌'
    print(fnee.cut_words(sentence))
