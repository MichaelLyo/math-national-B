import xlrd
import xlwt

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


dataWork = xlwt.Workbook()
d_sheet = dataWork.add_sheet('sheet1', cell_overwrite_ok=True)

for i in range(len(latitude_task)):
    d_sheet.write(i, 0, latitude_task[i])
    d_sheet.write(i, 1, longitude_task[i])
    new_price = 0
    if success[i]:
        new_price=price[i]+random.randint(0,5)*0.5
    else:
        new_price = price[i] + random.randint(6, 10) * 0.5
    d_sheet.write(i, 2, new_price)

dataWork.save('create_data.xls')