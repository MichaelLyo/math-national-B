import xlrd
import xlwt
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import *
from collections import defaultdict
import random

data_a = xlrd.open_workbook('a.xls')
table = data_a.sheets()[0]
ncols = table.ncols

latitude_task = table.col_values(1)
latitude_task = latitude_task[1:]

longitude_task = table.col_values(2)
longitude_task = longitude_task[1:]

price = table.col_values(3)
price = price[1:]

success = table.col_values(4)
success = success[1:]


# X = [[6, 2], [8, 1], [10, 0], [14, 2], [18, 0]]
# y = [[7], [9], [13], [17.5], [18]]

X = []
y = []
for i in range(len(latitude_task)):
    X.append([latitude_task[i],longitude_task[i],price[i]])
    y.append(success[i])

model = LinearRegression()
model.fit(X, y)

#print a

data_b = xlrd.open_workbook('create_data.xls')
table_b = data_b.sheets()[0]

latitude_b = table_b.col_values(0)
latitude_b = latitude_b[1:]

longitude_b = table_b.col_values(1)
longitude_b = longitude_b[1:]

price_b = table_b.col_values(2)
price_b = price_b[1:]


# X_test = [[8, 2], [9, 0], [11, 2], [16, 2], [12, 0]]
# y_test = [[11], [8.5], [15], [18], [11]]

X_test = []
y_test = []

for i in range(len(latitude_b)):
    X_test.append([latitude_b[i],longitude_b[i],price_b[i]])
    y_test.append(success[i])

predictions = model.predict(X)
for i, prediction in enumerate(predictions):
    print('Predicted: %s, Target: %s' % (prediction, y[i]))
print('R-squared: %.2f' % model.score(X, y))