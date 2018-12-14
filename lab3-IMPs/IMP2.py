import numpy as np
import sys
import random
import math
from functools import reduce
import operator
import time
import queue

### ------------global------------ ###
# parameters passed:
network_file_path = ''
k = 0
model_type = ''
time_budget = 0

# after processing:
network_file_list = []
n = 0  ### nodes number
m = 0  ### edges number

graph = []
nbr_dict = {}
reverse_nbr_dict = {}


### ------------global------------ ###


def init():
	global network_file_path
	global k
	global model_type
	global time_budget

	global network_file_list
	global n
	global m
	global graph
	global nbr_dict
	global reverse_nbr_dict

	global sample_time

	# network_file_path = sys.argv[2]
	# k = int(sys.argv[4])
	# model_type = sys.argv[6]
	# time_budget = sys.argv[8]
	network_file_path = './NetHEPT_fixed.txt'
	k = 5
	model_type = 'LT'  ##LT
	time_budget = 50
	network_file_list = open(network_file_path).readlines()

	n = int(network_file_list[0].split()[0])
	m = int(network_file_list[0].split()[1])

	### build the graph:
	graph = np.zeros((n + 1, n + 1), dtype=np.float)

	### build the neighbor dict
	for i in range(1, m + 1):
		v1 = int(network_file_list[i].split()[0])
		v2 = int(network_file_list[i].split()[1])
		graph[v1][v2] = float(network_file_list[i].split()[2])

		if v1 not in nbr_dict:
			nbr_dict[v1] = [v2]
		else:
			nbr_dict[v1].append(v2)

		if v2 not in reverse_nbr_dict:
			reverse_nbr_dict[v2] = [v1]
		else:
			reverse_nbr_dict[v2].append(v1)


def comb(n, k):
	return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def random_pick(some_list, probabilities):
	x = random.uniform(0, 1)

	cumulative_probability = 0.0
	for item, item_probability in zip(some_list, probabilities):
		cumulative_probability += item_probability
		if x < cumulative_probability: break
	return item


def generateRR_IC(v):
	RR = set()

	ActivitySet = [v]

	while (len(ActivitySet) != 0):
		time1 = time.time()
		newActivitySet = []
		for seed in ActivitySet:
			if seed not in reverse_nbr_dict:
				continue
			for neighbor in reverse_nbr_dict[seed]:
				if neighbor not in RR:
					probability = graph[neighbor][seed]
					state = random_pick([1, 0], [probability, 1 - probability])
					if state == 1:
						RR.add(neighbor)
						newActivitySet.append(neighbor)
		time2 = time.time()
		print(time2-time1)
		ActivitySet = newActivitySet

	return RR


def generateRR_LT(v):
	RR = set()

	ActivitySet = [v]

	while (len(ActivitySet) != 0):
		newActivitySet = []
		for seed in ActivitySet:
			other_probability = 1
			pick_list = []
			probability_list = []

			if seed not in reverse_nbr_dict:
				continue
			for neighbor in reverse_nbr_dict[seed]:
				if neighbor not in RR:
					pick_list.append(neighbor)
					probability_list.append(graph[neighbor][seed])
					other_probability -= graph[neighbor][seed]
			pick_list.append(-1)
			probability_list.append(other_probability)
			select_neighbor = random_pick(pick_list, probability_list)

			if select_neighbor != -1:
				RR.add(select_neighbor)
				newActivitySet.append(select_neighbor)
			else:
				return RR
		ActivitySet = newActivitySet

	return RR


def Sampling(e0, l):
	R = []
	LB = 1

	e = e0 * (2 ** 0.5)

	for i in range(1, int(math.log(n, 2))):
		x = n / pow(2, i)
		lmd1 = ((2 + (2 / 3) * e) * (math.log(comb(n, k)) + l * math.log(n) + math.log(math.log(n, 2))) * n) / pow(e, 2)
		sita_i = lmd1 / x

		while (len(R) <= sita_i):

			v = random.randint(1, n)
			RR = set()
			if model_type == 'IC':
				RR = generateRR_IC(v)
			elif model_type == 'LT':
				RR = generateRR_LT(v)
			if len(RR) != 0:
				R.append(RR)
			print(len(R))
		S_i = NodeSelection(R, k)

		_F_R = F_R(S_i, R)

		if (n * _F_R) >= ((1 + e) * x):
			LB = n * _F_R / (1 + e)
			break

	a = (l * math.log(n) + math.log(2)) ** 0.5
	b = ((1 - math.exp(-1)) * (math.log(comb(n, k)) + l * math.log(n) + math.log(2))) ** 0.5
	lmd2 = 200 * n * np.square((1 - math.exp(-1)) * a + b)
	sita = lmd2 / LB

	while (len(R) <= sita):
		v = random.randint(1, n)
		if model_type == 'IC':
			RR = generateRR_IC(v)
		elif model_type == 'LT':
			RR = generateRR_LT(v)
		if len(RR) != 0:
			R.append(RR)

	return R


def F_R(S_i, R):
	count = 0.0

	if S_i is None:
		return count
	for i in range(len(R)):
		### condider R[i]

		for seed in S_i:

			if seed in R[i]:
				count += 1
				break
	# return a fraction number: |RR| / |R|

	return (count / len(R))


def NodeSelection(R, k):
	freq_list = np.zeros(n + 1, dtype=np.int)
	for _RR in R:
		for i in _RR:
			freq_list[i] += 1

	V_set = set()
	for idx in range(1, n + 1):
		if freq_list[idx] != 0:
			V_set.add(idx)

	S_k = []

	q = queue.PriorityQueue()

	for v in V_set:
		q.put((-freq_list[v], 0, v))

	v0 = q.get()
	S_k.append(v0[2])

	# delete get()'s RR
	for _RR in R:
		if v0[2] in _RR:
			for r in _RR:
				freq_list[r] -= 1
				if freq_list[r] == 0:
					V_set.remove(r)

	iter = 1

	while (len(S_k) != k):

		if len(V_set) == 0:
			break

		# for v in V_set:
		#     marginal_gain = freq_list[v]
		#
		#     if marginal_gain > max:
		#         max = marginal_gain
		#         max_v = v
		#

		while (q.queue[0][1] != -iter):
			V = q.get()
			if V[2] not in V_set:
				continue

			marginal_gain = freq_list[V[2]]
			q.put((-marginal_gain, -iter, V[2]))

		max_V = q.get()
		iter += 1
		S_k.append(max_V[2])

		for _RR in R:
			if max_V[2] in _RR:
				for r in _RR:
					freq_list[r] -= 1
					if freq_list[r] == 0:
						V_set.remove(r)

	while (len(S_k) != k):
		node = random.randint(1, n)
		if node not in S_k:
			S_k.append(node)

	return S_k


def main():
	time1 = time.time()
	init()
	time2 = time.time()
	# print("ReadingTime",time2-time1)
	l = 1 + math.log(2) / math.log(n)  #### l = 1

	R = Sampling(0.2, l)  #### ipsilon = 0.1
	S_k = NodeSelection(R, k)

	print(S_k)
	# print(time.time()-time1)


if __name__ == '__main__':
	main()
