import copy
import random
allDemands = {(1,4):2,(4,1):2,(1,3):4,(3,1):4
			  ,(2,3):5,(3,2):5,(4,5):5,(5,4):5,(3,7):6,(7,3):6
			  ,(2,5):1,(5,2):1,(2,7):3,(7,2):3,(5,6):2,(6,5):2
			  }
depot = 1
capacity = 7
minCost = [[0,0,0,0,0,0,0,0],
		 [0,0,8,4,2,7,20,10],
		 [0,8,0,9,6,1,14,3],
		 [0,4,9,0,6,10,21,6],
		 [0,2,6,6,0,5,18,9],
		 [0,7,1,10,5,0,13,4],
		 [0,20,14,21,18,13,0,15],
		 [0,10,3,6,9,4,15,0]]
costs = [[0,0,0,0,0,0,0,0],
		 [0,0,0,4,2,0,0,0],
		 [0,0,0,10,8,1,0,3],
		 [0,4,10,0,0,0,0,6],
		 [0,2,8,0,0,5,0,0],
		 [0,0,1,0,5,0,13,0],
		 [0,0,0,0,0,13,0,15],
		 [0,0,3,6,0,0,15,0]]
IFINITY = 100000
def calculate(item1):

	Cost = 0
	for routes in item1:
		load = 0
		start = depot
		for (a,b) in routes:
			q = minCost[start][a]
			t = costs[a][b]
			start = b
			Cost+=(q+t)
		c = minCost[start][depot]
		Cost+=c
	return Cost

def singleInsertion(S):
	allCost = calculate(S)
	currentCost = 0
	currentSol = []
	for i in range(len(S)):
		for j in range(len(S[i])):
			for i2 in range(len(S)):
				for j2 in range(len(S[i2])+1):
					if i2 == i and j2 == j:
						continue
					value = S[i][j]
					list.insert(S[i2],j2,value)
					S[i].remove(value)
					currentCost = calculate(S)
					if(currentCost<allCost):
						allCost  = currentCost
						currentSol = copy.deepcopy(S)

					S[i2].remove(value)
					list.insert(S[i],j,value)
	while ([]in currentSol):
		currentSol.remove([])
	return currentSol

def doubleInsertion(S):
	allCost = calculate(S)
	currentCost = 0
	currentSol = []
	for i in range(len(S)):
		for j in range(len(S[i])-1):
			for i2 in range(len(S)):
				for j2 in range(len(S[i2])+1):
					if i2 == i and j2 == j:
						continue
					value1 = S[i][j]
					value2 = S[i][j+1]
					list.insert(S[i2], j2, value2)
					list.insert(S[i2], j2, value1)
					S[i].remove(value1)
					S[i].remove(value2)

					currentCost = calculate(S)

					if (currentCost < allCost):
						allCost = currentCost
						currentSol = copy.deepcopy(S)
						# print(currentCost)
						# print(S)
					S[i2].remove(value1)
					S[i2].remove(value2)
					list.insert(S[i], j, value2)
					list.insert(S[i], j, value1)

	while ([]in currentSol):
		currentSol.remove([])
	return currentSol


def swap(S):
	allCost = calculate(S)
	currentCost = 0
	currentSol = []
	for i in range(len(S)):
		for j in range(len(S[i])):
			for i2 in range(len(S)):
				for j2 in range(len(S[i2])):
					if i2 == i and j2 == j:
						continue
					# a,b = S[i][j]
					# a2,b2 = S[i2][j2]
					# if j == 0:
					# 	last = depot
					# else :
					# 	last,temp = S[i][j-1]
					# if j == len(S[i])-1:
					# 	next = depot
					# else:
					# 	temp,next = S[i][j+1]
					#
					# if j2 == 0:
					value1 = S[i][j]
					value2 = S[i2][j2]
					S[i].remove(value1)
					S[i2].remove(value2)
					list.insert(S[i2], j2, value1)
					list.insert(S[i], j, value2)

					currentCost = calculate(S)

					if (currentCost < allCost):
						allCost = currentCost
						currentSol = copy.deepcopy(S)

					S[i2].remove(value1)
					S[i].remove(value2)
					list.insert(S[i], j, value1)
					list.insert(S[i2], j2, value2)

	while ([]in currentSol):
		currentSol.remove([])
	return currentSol

def pathScaning(method):
	finalresult = []
	tempt = allDemands.copy()
	while(len(tempt)>0):
		routes = []
		leftCap = capacity
		while(True):
			if(len(routes)==0):
				start = depot
			else:
				(q,start) = routes[-1]
			closest = []
			for key,value in tempt.items():
				a,b = key
				if value>0 and value<=leftCap:
					if len(closest) == 0 :
						closest.append(key)
					else:
						a1,b1 = closest[0]
						if(minCost[start][a]<minCost[start][a1]):
							closest = []
							closest.append(key)
						elif(minCost[start][a] == minCost[start][a1]):
							closest.append(key)
			if(len(closest) == 0 ):
				break;
			if(len(closest) == 1 ):
				a,b = closest[0]
				result = (a,b)
				leftCap-=tempt.get((a,b))
				tempt.pop((a,b))
				tempt.pop((b,a))
			else:
				if method == 1:###maxmize the dis from the head to the depot
					maxdis = 0
					result = None
					for (a,b) in closest:
						if (minCost[depot][a]>maxdis):
							result = (a,b)
				elif method == 2:###minimize the dis from the head to the depot
					mindis = IFINITY
					result = None
					for (a, b) in closest:
						if (minCost[depot][a] < mindis):
							result = (a, b)
				elif method == 3:###maximize dem(t)/sc(t)
					demsc = 0
					result = None
					for (a, b) in closest:
						demsc2 = allDemands.get((a,b))/costs[a][b]
						if (demsc2 > demsc):
							result = (a, b)
				elif method == 4:###minimize dem(t)/sc(t)
					demsc = IFINITY
					result = None
					for (a, b) in closest:
						demsc2 = allDemands.get((a, b)) / costs[a][b]
						if (demsc2 < demsc):
							result = (a, b)
				elif method == 5:###if capacity <=0.5capacity then use method1 otherwise use method 2
					if leftCap<=0.5*capacity:
						maxdis = 0
						result = None
						for (a, b) in closest:
							if (minCost[depot][a] > maxdis):
								result = (a, b)
					else:
						mindis = IFINITY
						result = None
						for (a, b) in closest:
							if (minCost[depot][a] < mindis):
								result = (a, b)
				leftCap -= tempt.get(result)
				a,b = result
				tempt.pop(result)
				tempt.pop((b,a))
			routes.append(result)

		# print(routes)

		finalresult.append(routes)

	return finalresult
def calculate(item1):
	Cost = 0
	for routes in item1:
		load = 0
		start = depot
		for (a, b) in routes:
			load += allDemands.get((a, b))
			Cost += minCost[start][a]
			Cost += costs[a][b]
			start = b
		Cost += costs[start][depot]
	return Cost

def getCrossOver(task, routes):
	minGrade = IFINITY
	finalresult = []
	for i in range(len(routes)):
		list.insert(routes, i, task)
		temptGrade = calculate(list)
		if temptGrade < minGrade:
			finalresult = copy.deepcopy(routes)
		routes.remove(task)
	return finalresult


def crossOver(S1, S2):
	while True:
		r1 = random.randint(0, len(S1) - 1)
		r2 = random.randint(0, len(S2) - 1)
		R1 = S1[r1]
		R2 = S2[r2]

		r1 = random.randint(0, len(R1) - 1)
		R11 = R1[:r1]
		R12 = R1[r1:]

		r2 = random.randint(0, len(R2) - 1)
		# R21 = R2[:r2]
		R22 = R2[r2:]

		R1loss = []  ###the tasks that R1new don't have
		# R2loss = []###the tasks that R2new don't have

		###find out the lost one
		for (a, b) in R12:
			if ((a, b) not in R22) or ((b, a) not in R22):
				R1loss.append((a,b))
		# for (a,b) in R22:
		# 	if ((a,b) not in R21) or ((b,a) not in R21):
		# 		R2loss.append(i)

		###handle duplicate
		for (a, b) in R22:
			for q in S1:
				if (a, b) in q or (b, a) in q:
					R22.remove((a, b))
					break
		# for (a,b) in R12:
		# 	for q in S1:
		# 		if (a,b) in q or (b,a) in q :
		# 			R12.remove((a,b))
		# 			break

		RR1 = R11.append(R22)
		# RR2 = R21.append(R12)

		for i in R1loss:
			R1new = getCrossOver(i, RR1)
		# for i in R2loss:
		# 	R2new = getCrossOver(i,RR2)

		if calculate(R1new) > capacity:
			continue
		else:
			S1.remove(R1)
			# S2.remove(R2)
			S1.append(R1new)
			# S2.append(R2new)
			break
	return S1

b = [[(1, 35), (35, 34), (34, 27), (27, 28), (28, 35), (35, 36), (36, 37), (37, 31), (31, 30), (30, 37), (37, 38), (38, 4), (4, 5), (5, 39), (39, 38), (38, 31), (31, 32), (32, 39), (4, 3), (3, 37), (30, 29), (29, 36)], [(1, 11), (11, 12), (12, 13), (13, 18), (18, 22), (22, 21), (21, 24), (24, 25), (25, 22), (21, 20), (20, 23), (23, 24), (20, 17), (17, 18), (18, 19), (19, 13), (13, 7), (7, 3), (3, 2), (2, 36), (2, 1), (1, 6), (6, 12), (12, 17), (17, 13), (7, 6), (6, 2)], [(1, 8), (8, 9), (9, 15), (15, 16), (16, 11), (16, 10), (10, 1), (1, 40), (40, 8), (8, 14), (14, 15), (9, 10), (1, 33), (33, 34), (34, 26), (26, 27), (26, 33)]]
def check(sol,t):
	demands = copy.deepcopy(allDemands)
	for i in sol:
		for (a,b) in i:
			if demands[a][b]!=0:
				demands[a][b] = 0
			else:
				print(t)
			if demands[b][a]!=0:
				demands[b][a] = 0
			else:
				print(t)
check(b,'a')