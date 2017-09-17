# -*- coding: utf-8
import numpy as np
import urllib2
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

# 加载数据
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
raw_data = urllib2.urlopen(url)

# 把CSV文件转化为numpy matrix
dataset = np.loadtxt(raw_data, delimiter=",")
# 训练集和结果
x = dataset[:, 0:7]
y = dataset[:, 8]
# 数据归一化
normalized_x = preprocessing.normalize(x)
# 逻辑回归
model = LogisticRegression()

model.fit(normalized_x, y)

# 预测
expected = y
predicted = model.predict(normalized_x)

print predicted

# 模型拟合概述
print (metrics.classification_report(expected, predicted))
print "hello"
print (metrics.confusion_matrix(expected, predicted))