import time
import sys
import numpy as np
import random
from random import choice
import multiprocessing
import time
# Set Global Variables:
# numberrr = 0
start = 0
run_time = 0
termination = 0
random_seed = 0

vertices = 0
depot = 0
required_edges = 0  # task number!!!
# non_required_edges = 0
# vehicles = 0
capacity = 0
total_cost = 0  # 没啥用。。

actual_total_cost = 0  # FINAL RESULT COST !!!!! important!!!
# A list to store all  actual_total_cost (1000个) in order.
actual_total_cost_list = [0, ]

cost_matrix = []
demand_matrix = []

# 任意两点间的最短距离
min_dist = []

# 有任务的边 set of tuple (v1,v2)
free_set = set()

# A list to store all rotes
all_routes = []
# A list to store 所有的 all_routes （1000个）
all_routes_list = ['', ]

MAX_VALUE = 99999


# Set global variables
def set_globals(file_content_list):
	global vertices
	vertices_line = file_content_list[1].rstrip('\n')
	vertices = extract_digit(vertices_line)

	global depot
	depot_line = file_content_list[2].rstrip('\n')
	depot = extract_digit(depot_line)

	global required_edges
	required_edges_line = file_content_list[3].rstrip('\n')
	required_edges = extract_digit(required_edges_line)

	global non_required_edges
	non_required_edges_line = file_content_list[4].rstrip('\n')
	non_required_edges = extract_digit(non_required_edges_line)

	global vehicles
	vehicles_line = file_content_list[5].rstrip('\n')
	vehicles = extract_digit(vehicles_line)

	global capacity
	capacity_line = file_content_list[6].rstrip('\n')
	capacity = extract_digit(capacity_line)

	global total_cost
	total_cost_line = file_content_list[7].rstrip('\n')
	total_cost = extract_digit(total_cost_line)

	# After getting vertices number ==> cost_matrix (2d), demand_matrix(2d)
	global cost_matrix
	global demand_matrix
	cost_matrix = np.zeros((vertices + 1, vertices + 1), dtype=np.int)
	demand_matrix = np.zeros((vertices + 1, vertices + 1), dtype=np.int)

	set_cost_n_demand_matrix(file_content_list)

	# 任意两点间的最短距离
	global min_dist
	min_dist = np.zeros((vertices + 1, vertices + 1), dtype=np.int)
	# for x in range(vertices + 1):
	#     for y in range(vertices + 1):
	#         min_dist[x][y] = MAX_VALUE
	#         min_dist[y][x] = MAX_VALUE

	set_min_dist()

	global free_set
	set_free_set(file_content_list)


# Extract digits from string
def extract_digit(stri):
	res = ''
	for i in range(len(stri)):
		if stri[i].isdigit():
			res += stri[i]
	return int(res)


# Set cost matrix and demand matrix
def set_cost_n_demand_matrix(file_content_list):
	global cost_matrix
	global demand_matrix

	for i in range(len(cost_matrix)):
		for j in range(len(cost_matrix[i])):
			if i != j:
				cost_matrix[i][j] = MAX_VALUE
	cost_matrix[0][0] = MAX_VALUE

	length = len(file_content_list)
	# print(length)
	for i in range(9, length - 1):
		a = file_content_list[i].rstrip('\n')

		x = int(a.split()[0])

		y = int(a.split()[1])

		cost_matrix[x][y] = int(a.split()[2])
		cost_matrix[y][x] = int(a.split()[2])
		demand_matrix[x][y] = int(a.split()[3])
		demand_matrix[y][x] = int(a.split()[3])


# Set free set
def set_free_set(file_content_list):
	global free_set
	length = len(file_content_list)
	for i in range(9, length - 1):
		a = file_content_list[i].rstrip('\n')
		if int(a.split()[3]) != 0:
			# print(a.split()[3])
			x = int(a.split()[0])
			y = int(a.split()[1])
			free_set.add((x, y))
			free_set.add((y, x))


# Set min_dist
def set_min_dist():
	global min_dist
	global cost_matrix

	for i in range(len(cost_matrix)):
		for j in range(len(cost_matrix[i])):
			min_dist[i][j] = cost_matrix[i][j]

	find_v_2_all_sp2()
	# v_0 = 1
	# v_n = vertices
	#
	# for v in range(v_0, v_n + 1):
	#     # find v to every other nodes' shortest path:
	#     find_v_2_all_sp(v)


def find_v_2_all_sp2():
	global min_dist

	global vertices
	for k in range(1, vertices + 1):
		for i in range(1, vertices + 1):
			for j in range(1, vertices + 1):
				if (min_dist[i][j] > min_dist[i][k] + min_dist[k][j]):
					min_dist[i][j] = min_dist[i][k] + min_dist[k][j]


# Dijkstra Algorithm, start from v
def find_v_2_all_sp(v):
	global min_dist

	# keep a visit list: visit[i] is 0 ==> unvisited, 1 ==> visited
	not_visit = set()
	for i in range(1, (vertices + 1)):
		not_visit.add(i)

	# initialization:
	not_visit.remove(v)
	min_dist[v][v] = 0

	for other_v in range(vertices + 1):
		if cost_matrix[v][other_v] != 0:
			min_dist[v][other_v] = cost_matrix[v][other_v]
			min_dist[other_v][v] = cost_matrix[v][other_v]

	while len(not_visit) != 0:

		# for every other_v in not_visit set, find the one with min distance with v in min_dist[v][other_v]
		min = MAX_VALUE
		other_v_min = 0
		for other_v in not_visit:
			if min_dist[v][other_v] < min:
				other_v_min = other_v

		not_visit.remove(other_v_min)

		for i in range(1, vertices + 1):
			if cost_matrix[other_v_min][i] != 0:
				if min_dist[v][i] > min_dist[v][other_v_min] + cost_matrix[other_v_min][i]:
					min_dist[v][i] = min_dist[v][other_v_min] + cost_matrix[other_v_min][i]
					min_dist[i][v] = min_dist[v][other_v_min] + cost_matrix[other_v_min][i]


def path_scanning(i):
	global cost_matrix
	global demand_matrix
	global min_dist
	global free_set
	global all_routes

	global capacity
	global depot
	global actual_total_cost
	# global numberrr

	# print('----------',i,'---------')
	# print(free_set)
	free_set_copy = set()
	for s in free_set:
		free_set_copy.add(s)

	actual_total_cost = 0
	all_routes = []

	while len(free_set_copy) != 0:
		one_route = []
		start_node = depot
		load = 0
		cost = 0
		task_v_to = depot

		while load < capacity:
			# 更新 start_node, load, cost
			# 满足容量限制 且 最近 的set：
			consider_set = set()
			min_dist_value = MAX_VALUE
			# 完成consider_set的建立
			# consider_set里面装的都是距离最近的task：
			for task in free_set_copy:
				v_from = int(task[0])
				# v_to = int(task[1])
				# if demand_matrix[v_from][v_to] <= (capacity - load):  # 满足容量限制
				if min_dist[start_node][v_from] == min_dist_value:  # 与已有最近的task等价，也是最近的
					consider_set.add(task)
				elif min_dist[start_node][v_from] < min_dist_value:
					consider_set = set()
					consider_set.add(task)
					min_dist_value = min_dist[start_node][v_from]  # 找到了更近的task，更新consider_set和min_dist_value

			# l1 = len(consider_set)

			consider_set_copy = set()
			for s in consider_set:
				consider_set_copy.add(s)
			# 把不符合条件的去掉：
			for task in consider_set_copy:
				v_from = int(task[0])
				v_to = int(task[1])
				if demand_matrix[v_from][v_to] > (capacity - load):
					consider_set.remove(task)

			# l2 = len(consider_set)
			#
			# if l1 > l2:
			#     print(l1-l2)

			if len(consider_set) == 0:
				break

			# 选择一个task去执行
			task_choice = (-1, -1)
			# max_dist_value = -1
			# min_dist_value = MAX_VALUE

			if len(consider_set) == 1:
				for t in consider_set:
					task_choice = t
			# 距离最近的task有好几个
			elif len(consider_set) > 1:

				task_choice = choice(list(consider_set))

			if task_choice == (-1, -1):
				break
			# else:
			#     numberrr += 1

			# print('task choice:',task_choice)
			task_v_from = int(task_choice[0])
			task_v_to = int(task_choice[1])

			free_tuple1 = (task_v_from, task_v_to)
			free_tuple2 = (task_v_to, task_v_from)

			free_set_copy.remove(free_tuple1)
			free_set_copy.remove(free_tuple2)

			load = load + demand_matrix[task_v_from][task_v_to]
			cost = cost + min_dist[start_node][task_v_from] + cost_matrix[task_v_from][task_v_to]

			start_node = task_v_to

			one_route.append(task_choice)

		# print(one_route)
		all_routes.append(one_route)
		cost = cost + min_dist[task_v_to][depot]
		actual_total_cost += cost


def main():
	global start
	global run_time
	global termination
	global random_seed
	global cost_matrix
	global demand_matrix
	global all_routes
	global actual_total_cost

	start = time.time()

	# CARP_instance_file = '/Users/wangyutong/Repository/store/CS/大三上/人工智能/carp/Proj2_Carp/CARP_samples/egl-e1-A.dat'

	# CARP_instance_file = sys.argv[1]
	#
	# termination = sys.argv[3]
	#
	# random_seed = sys.argv[5]
	# random.seed(random_seed)
	CARP_instance_file = 'val7A.dat'

	# readlines()返回一个list
	file_content_list = open(CARP_instance_file).readlines()

	# 完成所有global的赋值，cost_matrix && demand_matrix && min_dist 的赋值 （均为2d数组）, free_set的赋值
	set_globals(file_content_list)
	# for i in demand_matrix:
	# 	print(i)
	# print(min_dist)
	# count = 0
	# for c_l in cost_matrix:
	#     for c in c_l:
	#         if c != 0:
	#             count+=1
	# # print(count)
	# print(min_dist)
	start_time = time.time()
	for i in range(1000):

		path_scanning(i)
		# print('all_routes:',all_routes)
		# print('---------------------------')
		all_routes_list.append(all_routes)
		actual_total_cost_list.append(actual_total_cost)
	end_time = time.time()
	print("totaltime",end_time-start_time)
	min_cost = MAX_VALUE
	min_idx = 0

	for i in range(1, 1001):
		print(actual_total_cost_list[i])
		if actual_total_cost_list[i] < min_cost:
			min_cost = actual_total_cost_list[i]
			min_idx = i

	all_routes = all_routes_list[min_idx]
	actual_total_cost = actual_total_cost_list[min_idx]

	# 接下来要用到：all routes & actual_total_cost
	res_line1 = ''
	res_line1 += 's '
	for i in range(len(all_routes)):
		# 得到 all_routes[i]
		res_line1 += '0,'
		for task in all_routes[i]:
			res_line1 += '(' + str(task[0]) + ',' + str(task[1]) + ')' + ','

		if i == len(all_routes) - 1:
			res_line1 += '0'
		else:
			res_line1 += '0,'

	print(res_line1)

	res_line2 = 'q ' + str(actual_total_cost)
	print(res_line2)

	# print(required_edges)
	# print(numberrr/500)

	# print(all_routes)

	# print('depot:',depot)
	# t_cost = 0
	#
	# for each_r in all_routes:
	#     print(each_r)
	#     start = depot
	#     each_demand = 0
	#     for each_t in each_r:
	#     #     print(each_t)
	#     # print('end')
	#         each_demand += demand_matrix[int(each_t[0])][int(each_t[1])]
	#         t_cost += min_dist[start][int(each_t[0])]
	#         t_cost += cost_matrix[int(each_t[0])][int(each_t[1])]
	#         start = int(each_t[1])
	#     print(each_demand)
	#     t_cost += min_dist[start][depot]
	#
	#
	# res_line2 = 'q ' + str(t_cost)
	# print(res_line2)

	run_time = time.time() - start
	# print(run_time)


if __name__ == '__main__':
	main()
