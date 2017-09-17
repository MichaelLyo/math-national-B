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

data_b = xlrd.open_workbook('b_new.xlsx')
table = data_b.sheets()[0]
gps = table.col_values(1)
gps = gps[1:]
latitude_mem = []
longitude_mem = []
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

    # if (temp_1 > 22 and temp_1 < 24.001):
    #     lat.append(temp_1)
    #     lon.append(temp_2)
    #     if (reputation[i] <= 19.0):
    #         lat_2.append(temp_1)
    #         lon_2.append(temp_2)
    #     elif (reputation[i] > 19.0):
    #         lat_3.append(temp_1)
    #         lon_3.append(temp_2)



#function to calculate distance
def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (0.5)


# function to calculate the variance of a group of data
def calculateVariance(x, y, avg):
    sum = 0
    for i in range(len(x)):
        sum += (getPrice(x[i],y[i]) - avg) ** 2
    result = (sum / len(x))**(0.5)
    return result

def avgPrice(x, y):
    sum = 0
    for i in range(len(x)):
        sum += getPrice(x[i],y[i])
    result = sum / len(x)
    return result

def getPrice(x, y):
    for item in all_points:
        if (x==item[0])&(y==item[1]):
            return item[3]
    return 0

# to judge whether a point is arounded by many members
def judge(point):
    judge_radius = 0.045
    count = 0
    for i in range(len(latitude_mem)):
        if dist(point, [latitude_mem[i], longitude_mem[i]]) < judge_radius:
            count += 1
    return count
    pass

def classify(mem_point):
    min_dis = 100
    for item in all_points:
        distance_m_p = dist(mem_point,item)
        if distance_m_p < min_dis:
            min_dis = distance_m_p
    for item in all_points:
        if dist(item, mem_point) == min_dis:
            item[5].append(mem_point)
    pass

# get the central point of a group of points
def getCentral(x, y):
    sum_x = 0
    sum_y = 0
    for i in range(len(x)):
        sum_x+=x[i]
        sum_y+=y[i]
    return [sum_x/len(x), sum_y/len(y)]

# get the mode of a group of points
def getMode(arr):
    counts = defaultdict(lambda: 0)
    for item in arr:
        counts[item] += 1
    max_value = 0
    mode = 0
    for key in counts:
        if counts[key]>max_value:
            max_value=counts[key]
            mode=key
    return mode

def getAlpha(cluster):
    alpha = []
    mode_num = 0
    density_amount = 0
    count_zero=0
    for j_1 in range(len(cluster[2])):
        if cluster[2][j_1] == cluster[6]:
            mode_num += 1
            density_amount += cluster[3][j_1]
    density_avg = density_amount/mode_num
    for i_1 in range(len(cluster[2])):
        if cluster[2][i_1] != cluster[6]:
            factor = float(cluster[3][i_1]) / density_avg
            #print "factor:",factor, "price: ", cluster[2][i_1], "mode: ", cluster[5], "density:",cluster[3][i_1]
            if(factor!=0):
                newItem = (cluster[2][i_1] - cluster[6]) / factor
                alpha.append([newItem,cluster[5][i_1]])
            else:
                count_zero+=1
    print "zero have ", count_zero
    return alpha


# calculate distance
def calAvgDis(points):
    sum = 0
    length = len(points)
    count_num = 0
    for count_cal in range(length):
        if count_cal< length - 1:
            for j_cal in range(count_cal+1,length):
                sum += dist(points[count_cal],points[j_cal])
                count_num += 1
    return sum/count_num

# take radius = 8 and min. points = 8
eps = 0.04500000
minPts = 1
#eps = 0.1
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


for i in range(len(longitude_mem)):
    classify([latitude_mem[i], longitude_mem[i]])

mywork = xlwt.Workbook()
mysheet = mywork.add_sheet(u'sheet1', cell_overwrite_ok=True)
for j in range(len(all_points)):
    mysheet.write(j,0,latitude_task[j])
    mysheet.write(j,1,longitude_task[j])
    mysheet.write(j,2,price[j])
    mysheet.write(j,3,success[j])
    mysheet.write(j,4,len(all_points[j][5]))
    mysheet.write(j,5,all_points[j][4])

mywork.save('memberNum.xls')

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
markers = [[0 for col in range(4)] for row in range(7)]
markers[0] = ['b.', 'g.', 'r.', 'c.', 'm.', 'y.', 'k.']
markers[1] = ['b*', 'g*', 'r*', 'c*', 'm*', 'y*', 'k*']
markers[2] = ['b^', 'g^', 'r^', 'c^', 'm^', 'y^', 'k^']
markers[3] = ['b<', 'g<', 'r<', 'c<', 'm<', 'y<', 'k<']

# plotting the clusters
i = 0
count = 0
cluster_num = len(cluster_list)
transparency = 1.0/(cluster_num/7.0)

f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)

al_work = xlwt.Workbook()
al_sheet = al_work.add_sheet('sheet1', cell_overwrite_ok=True)
al_count = 0

#print cluster_list
for value in cluster_list:
    cluster = cluster_list[value]
    # print "cluster is:", cluster
    # print "cluster x is :", cluster[0]
    # print "cluster y is :", cluster[1]
    plot(cluster[1], cluster[0], markers[0][i % 7], alpha=transparency*(random.randint(1, (cluster_num/7))))
    # for x in range(len(cluster[0])):
    #     sign = (cluster[3][x]/3)%4
    #     plot(cluster[1][x],cluster[0][x],markers[sign][i%7])
    # print "my point:",cluster[0],cluster[1]
    #plot(cluster[0], cluster[1], 'ro')
    i = (i + 1)

    mem_num = 0

    for item in cluster[4]:
        mem_num += item

    count += 1
    avg = avgPrice(cluster[0], cluster[1])
    cent = getCentral(cluster[0], cluster[1])
    modes = getMode(cluster[2])

    cluster.append(modes)
    thisAlpha = getAlpha(cluster)
    #print "this cluster's alpha are: ", thisAlpha

    for al_it in thisAlpha:
        al_sheet.write(al_count, 0, al_it[0])
        al_sheet.write(al_count, 1, al_it[1])
        al_count+=1

    sheet1.write(i, 0, cent[0])
    sheet1.write(i, 1, cent[1])
    sheet1.write(i, 2, modes)
    sheet1.write(i, 3, mem_num)
    # sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))

    print "central point: ", cent
    print "mode is : ", modes
    print "member number is : ", mem_num, '\n'
    #print "\n\naverage price is:", avg
    # print "all price is:"
    # for g in range(len(cluster[0])):
    #     print getPrice(cluster[0][g], cluster[1][g])," ",
    # print "\nvarience is :", calculateVariance(cluster[0], cluster[1], avg), "  ",

f.save('mode.xls')
al_work.save('alpha.xls')
print "\neps is: ", eps, "minPts: ", minPts, "  count is:", count

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
plot(noisey, noisex, "x")
print "noisy points: ", len(noise_points)

#plot(latitude_mem, longitude_mem, 'y+')

title(str(len(cluster_list)) + " clusters created with eps =" + str(eps) + " Min Points=" + str(
    minPts) + " total points=" + str(len(all_points)) + " noise Points = " + str(len(noise_points)))


print "failed points' information:"
for i in range(len(success)):
    if not success[i]:
        print "price: ", price[i], " mem density:", all_points[i][4],
        if all_points[i][2] != 0:
            print "cluster mode: ", getMode(cluster_list[all_points[i][2]][2])

#show()



