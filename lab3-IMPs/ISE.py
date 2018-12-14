import sys
import numpy as np
import random
import copy
import time
import multiprocessing


def get_opt():
	address = sys.argv[2]
	seed_set = sys.argv[4]
	differential_model = sys.argv[6]
	time_budget = sys.argv[8]

	return address, seed_set, differential_model, time_budget


def read_file(path, type):
	lines = open(path)
	if type == 'network':
		line = lines.readline()
		nodes, edges = line.split(' ')[0:2]
		network = np.zeros((int(nodes) + 1, int(nodes) + 1))
		neighbors = {}
		invneighbors = {}
		for i in lines.readlines():
			network[int(i.split()[0])][int(i.split()[1])] = float(i.split()[2])
			if int(i.split()[0]) not in neighbors:
				neighbors[int(i.split()[0])] = [int(i.split()[1])]
			else:
				neighbors[int(i.split()[0])].append(int(i.split()[1]))

			if int(i.split()[1]) not in invneighbors:
				invneighbors[int(i.split()[1])] = [int(i.split()[0])]
			else:
				invneighbors[int(i.split()[1])].append(int(i.split()[0]))

		return network, invneighbors, neighbors, int(nodes)
	else:
		seed_set = []
		for i in lines.readlines():
			seed_set.append(int(i))

		return seed_set



def IC(network, neighbors, seed_set):
	activity_set = seed_set
	count = len(seed_set)
	activited = set()
	for i in seed_set:
		activited.add(i)
	while (len(activity_set) > 0):
		new_activity_set = []
		for seed in activity_set:
			if seed in neighbors:
				for i in neighbors[seed]:
					if (i not in activited):
						t = random.random()
						if (network[seed][i] > t):
							activited.add(i)
							new_activity_set.append(i)
		count += len(new_activity_set)
		activity_set = (new_activity_set)
	return count


def LT(network, invneighbors, neighbors, n, seed_set):
	thresh = np.zeros(n + 1)
	activity_set = (seed_set)
	activited = set()
	for i in activity_set:
		activited.add(i)
	for i in range(1, len(thresh)):
		t = random.random()
		thresh[i] = t
		if (t == 0):
			activity_set.append(i)
			activited.add(i)
	while (len(activity_set) > 0):
		new_activity_set = []
		for seed in activity_set:
			if seed in neighbors:
				for i in neighbors[seed]:
					w_total = 0
					if i not in activited:
						if i in invneighbors:
							for t in invneighbors[i]:
								if (t in activited) and network[t][i] > 0:
									w_total += network[t][i]
							if (w_total >= thresh[i]):
								new_activity_set.append(i)
								activited.add(i)

		activity_set = (new_activity_set)
	return len(activited)


def ISE(type, network, invneighbors, neighbors, n, seed_set,t,return_dict):
	sum = 0
	for i in range(0, 1250):
		if type == 'IC':
			sample = IC(network, neighbors, seed_set)
		else:
			sample = LT(network, invneighbors, neighbors, n, seed_set)
		sum += sample
	return_dict[t] = sum/1250
if __name__ == "__main__":
	test = True
	if test:
		address = './Gnutella30.txt'
		# seed_path = './seeds.txt'
		differential_model = 'LT'  ##LT
		time_budget = 50
	else:
		address, seed_path, differential_model, time_budget = get_opt()
	time1 = time.time()

	network, invneighbors, neighbors, n = read_file(address, 'network')
	# seed_set = read_file(seed_path, 'seed')
	seed_set = [4131,619,44,1168,531]
	all_result = []
	return_dict = multiprocessing.Manager().dict()

	for i in range(8):
		all_result.append(multiprocessing.Process(target=ISE,args=(differential_model, network, invneighbors, neighbors, n, seed_set,i,return_dict)))
		all_result[i].start()
	for i in all_result:
		i.join()
	time2 = time.time()
	print('total',time2-time1)
	sum = 0
	for i in return_dict.values():
		sum+=i
	print(sum/8)


