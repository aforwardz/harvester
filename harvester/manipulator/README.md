# manipulator
文本标注后台，提供前端接口

# 说明
1. 训练文本

文本数据的概念是以“文章”为单位，可以将其切为段落，段落可以切分为句子，句子可以切分为词

也就是说到words这里，应该是一个三维list；paragraph是二维list

# 文本分类
## 基于Sklearn
- [使用sklearn + jieba中文分词构建文本分类器](http://myg0u.com/%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/2015/05/06/use-sklearn-jieba.html)

## 基于Tensorflow
### 使用神经网络
- [CNN模型](http://www.jeyzhang.com/tensorflow-learning-notes-2.html)
- [利用TensorFlow实现卷积神经网络做文本分类](https://www.jianshu.com/p/ed3eac3dcb39)
- [Tensorflow实现CNN文本分类](https://www.jianshu.com/p/ff8e5f4635cc)
- [CNN与RNN中文文本分类-基于TensorFlow实现](https://gaussic.github.io/2017/08/30/text-classification-tensorflow/)
- [在TensorFlow中实现文本分类的卷积神经网络](http://www.tensorflownews.com/2017/08/21/implementing-a-cnn-for-text-classification-in-tensorflow/)

### 使用在线学习
- [tensorflow实现基于LSTM的文本分类方法](http://blog.csdn.net/u010223750/article/details/53334313)
