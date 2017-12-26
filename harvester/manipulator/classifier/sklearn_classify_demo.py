import jieba
import csv
import sklearn.feature_extraction
import sklearn.naive_bayes as nb
import sklearn.externals.joblib as jl
import sys


def predict(txt):
    kv = [t for t in jieba.cut(txt)]
    mt = fh.transform([kv])
    num = gnb.predict(mt)
    for (k, v) in catedict.items():
        if v == num:
            print(" do you mean...%s" % k)


def clipper(txt):
    return jieba.cut(txt)


if __name__ == '__main__':
    # Load file.
    reader = csv.reader(open('catedict.csv'))
    catedict = {}
    catelist = []
    memolist = []
    # The target category. suck as 1 -> "晚餐"  , 2 -> "午餐"
    for i in reader:
        catelist += [[i[0], int(i[1])]]
    catedict = dict(catelist)
    # init vars
    # the train data frame.
    reader = open('finished.csv', 'r')
    ctr = 0
    # that MODEL.
    gnb = nb.MultinomialNB(alpha=0.01)
    # Hashing Trick, transfrom dict -> vector
    fh = sklearn.feature_extraction.FeatureHasher(n_features=15000, non_negative=True, input_type='string')
    kvlist = []
    targetlist = []
    # use partial fitting because of big data frame.
    for col in reader:
        line = col.split(',')
        if len(line) == 2:
            line[1].replace('\n', '')
            kvlist += [[i for i in clipper(line[0])]]
            targetlist += [int(line[1])]
            ctr += 1
            sys.stdout.write('\r' + repr(ctr) + ' rows has been read   ')
            sys.stdout.flush()
        if ctr % 100000 == 0:
            print("\npartial fitting...")
            X = fh.fit_transform(kvlist)
            gnb.partial_fit(X, targetlist, classes=[i for i in catedict.values()])
            # clean context
            result = gnb.predict(X)
            rate = (result == targetlist).sum() * 100.0 / len(result) * 1.0
            print("rate %.2f %% " % rate)
            targetlist = []
            kvlist = []

    # finally , save the model
    jl.dumps(gnb, 'final.pkl')
    # you can use the model and feature hasher another place to predict text category.
