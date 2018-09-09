#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : Wed May  2 21:09:46 DST 2018
# @Author  : yangjintao

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rd
import math as mh

G=nx.Graph() #创建了一个没有节点和边的空图

posi=pd.read_excel("./2015Cities-CHINA_modify20180323.xlsx") # 读取数据

# 原始数据有337组数据，我只选择了268个城市的数据
lat = np.array(posi["lat"][0:268],dtype=float)    # 获取维度之维度值
lon = np.array(posi["lon"][0:268],dtype=float)    # 获取经度值
pop = np.array(posi["pop"][0:268],dtype=float)    # 获取人口数，转化为numpy浮点型
road_density = np.array(posi["density2012"][0:268],dtype=float)

pos = []#元组中的两个数字是第i（从0开始计数）个点的坐标  
#加点
for i in range(268):
	pos.append((lon[i],lat[i]))	
print("\n**************************************************************\n")
print("\t\t城市坐标：\n")
print("**************************************************************\n")
print("节点数：",len(pos),"\n")
print(pos)

#加边
edge_list = []	#原始边列表
for i in range(5000):
	m = rd.randint(0,267)
	n = rd.randint(0,267)
	#权重
	pop_weight = (pop[m]+pop[n])
	distance_weight = mh.sqrt((pos[m][0]-pos[n][0])**2+(pos[m][1]-pos[n][1])**2)
	#排除自己连自己情况,远距离连接情况
	if m != n and distance_weight < 40:
		edge_list.append((m,n,pop_weight/distance_weight**(0)))

sum_weight = 0
for i in range(len(edge_list)):
	sum_weight += edge_list[i][2]	#权重和
average_weight = sum_weight/len(edge_list)	#平均权重
#新边列表
new_edge_list = []
for i in range(len(edge_list)):
	if edge_list[i][2] > average_weight*1.5:	#大于平均权重的x倍加入新的边列表
		new_edge_list.append(edge_list[i])		#即去掉权重较小的边

print("\n**************************************************************\n")
print("\t\t边及其权重：\n")
print("**************************************************************\n")
print(new_edge_list,"\n")
print("边数：",len(new_edge_list),"\n")

G.add_weighted_edges_from(new_edge_list)	#加边
#画网络图
nx.draw_networkx(G,pos,with_labels=True,node_size = pop/np.max(pop)*50,node_color='blue')

print("\n**************************************************************\n")
print("\t\t节点度中心系数:\n")
print("**************************************************************\n")
print(nx.degree_centrality(G))	#节点度中心系数
print("\n**************************************************************\n")
print("\t\t图或网络中节点的聚类系数:\n")
print("**************************************************************\n")
print(nx.clustering(G))		#图或网络中节点的聚类系数

plt.title("networkx_demo_pop_roadnetwork_distance")
plt.xlim(75,140)
plt.ylim(10,55)

degree = nx.degree_histogram(G)          #返回图中所有节点的度分布序列
x = range(len(degree))                   #生成x轴序列，从1到最大度
y = [z / float(sum(degree)) for z in degree]
#将频次转换为频率，这用到Python的一个小技巧：列表内涵

# figure 2
plt.figure()
plt.title("degree distribution")
plt.xlabel("k")
plt.ylabel("P(k)")
plt.loglog(x,y,color="red",linewidth=2) #在双对数坐标轴上绘制度分布曲线

plt.show()
