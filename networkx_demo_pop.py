#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : Sa March  17 12:01:27 DST 2018
# @Author  : yangjintao

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rd
import math as mh

G=nx.Graph()  #方法生成一个空图

posi=pd.read_excel("./2015Cities-CHINA_modify20180323.xlsx") # 读取数据

# 原始数据有337组数据，我只选择了268个城市的数据
lat = np.array(posi["lat"][0:268],dtype=float)                  # 获取纬度值
lon = np.array(posi["lon"][0:268],dtype=float)                  # 获取经度值
pop = np.array(posi["pop"][0:268],dtype=float)    				# 获取人口数，转化为numpy浮点型

  
#******************************************************************
#								加点
#******************************************************************
nodes_list = [] 
pos = []#元组中的两个数字是第i（从0开始计数）个点的坐标
for i in range(268):
	nodes_list.append(i)
	pos.append((lon[i],lat[i]))	
print("\n**************************************************************\n")
print("\t\t城市坐标：\n")
print("**************************************************************\n")
print("节点数：",len(pos),"\n")
print(pos)


#******************************************************************
#								加边
#******************************************************************
initial_repeated_nodes = []
for i in range(len(nodes_list)):
	initial_repeated_nodes.extend([nodes_list[i]]*int(pop[i]/10))
	
repeated_nodes = []			#节点重复次数正比于人口数
old_nodes_list = []			#联通网络节点列表
weighted_edges_list = []	#边列表
m = rd.choice(initial_repeated_nodes)	#初始时刻按节点权重随机选点
old_nodes_list.append(m)
repeated_nodes.extend([old_nodes_list[-1]]*int(pop[m]/10))
for i in range(267):
	new_nodes_list = list(set(nodes_list)-set(old_nodes_list))		#新节点列表
	n = rd.choice(new_nodes_list)									#随机选择新节点
	for i in range(1):												#每一步加n条边
		target = rd.choice(repeated_nodes)							#随机选择已联通的网络里的节点做为目标节点
		distance_weight = mh.sqrt((pos[target][0]-pos[n][0])**2+(pos[target][1]-pos[n][1])**2)
		if distance_weight < 20:
			weighted_edges_list.append((n,target,pop[target]))		#连接新节点与目标节点
	old_nodes_list.append(n)
	repeated_nodes.extend([old_nodes_list[-1]]*int(pop[n]/10))

print("\n**************************************************************\n")
print("\t\t边及其权重：\n")
print("**************************************************************\n")
print(weighted_edges_list,"\n")
print("边数：",len(weighted_edges_list),"\n")
#加边
G.add_weighted_edges_from(weighted_edges_list)	
#画网络图
nx.draw_networkx(G,pos,with_labels=True,node_size = pop/np.max(pop)*50,node_color='blue')

print("\n**************************************************************\n")
print("\t\t节点度中心系数:\n")
print("**************************************************************\n")
print(nx.degree_centrality(G))			#节点度中心系数
print("\n**************************************************************\n")
print("\t\t图或网络中节点的聚类系数:\n")
print("**************************************************************\n")
print(nx.clustering(G))					#图或网络中节点的聚类系数

plt.title("networkx_demo_pop_roadnetwork")
plt.xlim(75,140)
plt.ylim(10,55)


degree = nx.degree_histogram(G)          #返回图中所有节点的度分布序列
x = range(len(degree))                   #生成x轴序列，从1到最大度
y = [z / float(sum(degree)) for z in degree]
#将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便

# figure 2
plt.figure()
plt.title("degree distribution")
plt.xlabel("k")
plt.ylabel("P(k)")
plt.loglog(x,y,color="red",linewidth=2)  #在双对数坐标轴上绘制度分布曲线

plt.show()
