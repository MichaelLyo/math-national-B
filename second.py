import xlrd
import xlwt

from matplotlib.pyplot import *
from collections import defaultdict

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

data_b = xlrd.open_workbook('b_new.xlsx')
table_b = data_b.sheets()[0]
gps = table_b.col_values(1)
gps = gps[1:]
latitude_mem = []
longitude_mem = []
distribution = table_b.col_values(6)
distribution = distribution[1:]
temp = table_b.col_values(7)
temp = temp[1:]

validation = []

for i in range(len(gps)):
    j = 0
    temp_1 = ''
    temp_2 = ''
    while (gps[i][j] != ' '):
        temp_1 += gps[i][j].encode("utf-8")
        j += 1

    j += 1

    while (j < len(gps[i])):
        temp_2 += gps[i][j].encode("utf-8")
        j += 1

    temp_1 = float(temp_1)
    temp_2 = float(temp_2)
    if (temp_1 > 22 and temp_1 < 24.001):
        latitude_mem.append(temp_1)
        longitude_mem.append(temp_2)
    else:
        del(distribution[i])
        del(temp[i])

for i in range(len(distribution)):
    print distribution[i], " ", temp[i]
    validation.append([latitude_mem[i], longitude_mem[i], distribution[i] * temp[i] / 10])


#function to calculate distance
def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (0.5)



# to judge the validation of the members surrounding the point
def judge(point):
    judge_radius = 0.045
    count = 0
    for i in range(len(latitude_mem)):
        if dist(point, [latitude_mem[i], longitude_mem[i]]) < judge_radius:
            count += validation[i][2]
    return count
    pass


# take radius = 8 and min. points = 8
eps = 0.04500000
minPts = 1

all_points = []

for i in range(len(longitude_task)):
    newPoint = [latitude_task[i], longitude_task[i]]
    all_points.append(newPoint)


other_points = []
core_points = []
plotted_points = []
count_p = 0

# find out the core points
for point in all_points:
    point.append(0)                 # assign initial level 0
    point.append(price[count_p])    # add the price of this point
    point.append(judge(point))      # add the members number level of this point
    point.append([])                # to store the members that close to it
    point.append(success[count_p])  # add the success information of this point
    count_p += 1
    totalChildPoints = 0
    for otherPoint in all_points:
        distance = dist(otherPoint, point)
        if distance <= eps:
            totalChildPoints += 1

    if totalChildPoints > minPts:
        core_points.append(point)
        plotted_points.append(point)
    else:
        other_points.append(point)

def getS_price(start, end, arr):
    mydict = defaultdict(lambda:0)
    for item in arr:
        if (item[4] < end) & (item[4] > start):
            mydict[item[3]] += 1
    maxK = 0
    key_m = 0
    for key in mydict:
        if mydict[key]>maxK:
            maxK = mydict[key]
            key_m=key
    return key_m


al_work = xlwt.Workbook()
sheet1 = al_work.add_sheet('sheet1', cell_overwrite_ok=True)
count_sh = 0

succ_arr = []
for item in all_points:
    if item[6]:
        succ_arr.append(item)

for point in all_points:
    sheet1.write(count_sh, 0, point[0])
    sheet1.write(count_sh, 1, point[1])
    sheet1.write(count_sh, 2, point[4])
    sheet1.write(count_sh, 3, point[3])
    standard_start = point[4]
    if not point[6]:

        stand_factor = 0
        modified_price = getS_price(standard_start-stand_factor, standard_start+1+stand_factor, succ_arr)
        while((modified_price<=point[3])&(stand_factor<100)):
            stand_factor+=1
            modified_price = getS_price(standard_start - stand_factor, standard_start + 1 + stand_factor, succ_arr)
        if(modified_price<point[3]):
            modified_price=point[3]
        sheet1.write(count_sh, 4, modified_price)
        print point[0], " ", point[1], " validation:",  point[4],"price:", point[3]
    else:
        sheet1.write(count_sh, 4, point[3])
    count_sh += 1

al_work.save('problem2.xls')

# find border points
border_points = []
for core in core_points:
    for other in other_points:
        if dist(core, other) <= eps:
            border_points.append(other)
            plotted_points.append(other)
print "core points: ", len(core_points)

# implement the algorithm
cluster_label = 0

for point in core_points:
    if point[2] == 0:
        cluster_label += 1
        point[2] = cluster_label

    for point2 in plotted_points:
        distance = dist(point2, point)
        if point2[2] == 0 and distance <= eps:
            # print point, point2
            point2[2] = point[2]

# after the points are asssigned correnponding labels, we group them
cluster_list = defaultdict(lambda: [[], [], [], [], [], []])

for point in plotted_points:
    cluster_list[point[2]][0].append(point[0])
    cluster_list[point[2]][1].append(point[1])
    cluster_list[point[2]][2].append(point[3])    # price
    cluster_list[point[2]][3].append(point[4])    # level
    cluster_list[point[2]][4].append(len(point[5]))  # the number of members around the point
    cluster_list[point[2]][5].append(point[6])


# plotting the clusters
i = 0
count = 0
cluster_num = len(cluster_list)
transparency = 1.0/(cluster_num/7.0)

new_all_points = []

for value in cluster_list:
    cluster = cluster_list[value]
    i = (i + 1)

    mem_num = 0

    for item in cluster[4]:
        mem_num += item

    count += 1


# plot the noise points as well
noise_points = []
for point in all_points:
    if not point in core_points and not point in border_points:
        noise_points.append(point)
noisex = []
noisey = []
for point in noise_points:
    noisex.append(point[0])
    noisey.append(point[1])
    new_all_points.append([point[0], point[1], point[3]])
#plot(noisey, noisex, "x")



#show()
