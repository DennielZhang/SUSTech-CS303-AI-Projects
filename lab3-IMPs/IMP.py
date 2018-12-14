import sys
import numpy as np
import random
import copy
import math
from functools import reduce
import operator
import heapq
import time

def c(n, k):
	return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def get_opt():
	address = sys.argv[2]
	k = sys.argv[4]
	differential_model = sys.argv[6]
	time_budget = sys.argv[8]
	return address, int(k), differential_model, int(time_budget)


def LT(network, invneighbors, seed_set):
	RR = set()
	activity_set = seed_set
	for i in seed_set:
		RR.add(i)
	while (len(activity_set) > 0):
		new_activity_set = []
		for seed in activity_set:
			num = random.random()
			start = 0
			if seed in invneighbors:
				for i in invneighbors[seed]:
					if (start <= num <= start + network[i][seed]):
						if i not in RR:
							RR.add(i)
							new_activity_set.append(i)
							break
					start = start + network[i][seed]
		activity_set = new_activity_set
	return RR


def IC(network, invneighbors, seed_set):
	activity_set = seed_set
	RR = set()
	for i in seed_set:
		RR.add(i)
	while (len(activity_set) > 0):
		new_activity_set = []
		for seed in activity_set:
			if seed in invneighbors:
				for i in invneighbors[seed]:
					if (i not in RR ) :
						t = random.random()
						if (network[i][seed] > t):
							RR.add(i)
							new_activity_set.append(i)
		activity_set = (new_activity_set)
	return RR


def GenerateRR(network, invneighbors, v, pattern):

	if pattern == 'LT':
		RR = LT(network, invneighbors, {v})
	else:
		RR = IC(network, invneighbors, {v})
	return RR


def FR(Si, R):
	count = 0
	for t in R:
		if t&Si!=set():
			count += 1
	return count / len(R)


def Sampling(network, invneighbors, k, e, l, n, pattern):
	R = []
	LB = 1
	e1 = 2 ** 0.5 * e
	for i in range(1, int(math.log(n, 2)) + 1):
		x = n / math.pow(2, i)
		lambda1 = (2 + 2 / 3 * e1) * (math.log(c(n, k)) + l * math.log(n) + math.log(math.log(n, 2))) * n / math.pow(e1,
																													 2)
		theata = lambda1 / x
		print(theata)
		while (len(R) <= theata):
			print(len(R))
			v = random.randint(1, n)
			RRs = GenerateRR(network, invneighbors, v, pattern)

			if RRs != set():
				R.append(RRs)
		S = NodeSelection(R, k, n)
		Fr = FR(S, R)
		if n * Fr >= (1 + e1) * x:
			LB = n * Fr / (1 + e1)
			break
	a = math.sqrt((l * math.log(n) + math.log(2)))
	b = math.sqrt((1 - 1 / math.e) * (math.log(c(n, k)) + l * math.log(n) + math.log(2)))
	lambdax = 2 * n * math.pow(((1 - 1 / math.e) * a + b), 2) * math.pow(e, -2)
	theata = lambdax / LB
	while (len(R) <= theata):
		v = random.randint(1, n)
		RRs = GenerateRR(network, invneighbors, v, pattern)
		R.append(RRs)
	return R


def NodeSelection(R, k, n):
	Sk = set()
	maxheap = []
	availablePoint = np.zeros(n+1)

	for i in R:
		for t in i :
			availablePoint[t] += 1

	for i in range(len(availablePoint)):
		if availablePoint[i]>0:
			t = (-availablePoint[i], i, 0)
			heapq.heappush(maxheap, t)

	for i in range(k):
		while (len(maxheap) > 0):
			(grade, Si, index) = heapq.heappop(maxheap)
			if(availablePoint[Si]>0):
				if (index == i):
					Sk.add(Si)
					for RR in R:
						if(Si in RR):
							for t in RR:
								availablePoint[t]-=1
					break
				t = (-availablePoint[Si], Si, i)
				heapq.heappush(maxheap, t)
	return Sk


def IMM(network,invneighbors, k,e,l, n, differential_model):
	l = l * (1 + math.log(2) / math.log(n))
	R = Sampling(network, invneighbors,k, e, l, n, differential_model)
	S = NodeSelection(R, k, n)
	return S


def read_file(path):
	lines = open(path)
	line = lines.readline()
	nodes, edges = line.split(' ')[0:2]
	network = np.zeros((int(nodes) + 1,int(nodes)+1))
	invneighbors = {}

	for i in lines.readlines():
		network[int(i.split()[0])][int(i.split()[1])] = float(i.split()[2])
		if int(i.split()[1]) not in invneighbors:
			invneighbors[int(i.split()[1])] = [int(i.split()[0])]
		else:
			invneighbors[int(i.split()[1])].append(int(i.split()[0]))


	return network,invneighbors, int(nodes)



if __name__ == "__main__":
	test = True

	if test:
		address = './Gnutella30.txt'
		k = 5
		differential_model = 'LT'  ##LT
		time_budget = 50
	else:
		address, k, differential_model, time_budget = get_opt()
	network, invneighbors, n = read_file(address)
	i1 = time.time()
	S = IMM(network,invneighbors, k, 0.1, 1, n, differential_model)
	i2 = time.time()
	print('total',i2-i1)
	for i in S:
		print(i)
	# print(S)
