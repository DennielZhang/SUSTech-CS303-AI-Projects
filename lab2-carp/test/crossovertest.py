import random
import copy

allDemands = {(1, 4): 2, (4, 1): 2, (1, 3): 4, (3, 1): 4
	, (2, 3): 5, (3, 2): 5, (4, 5): 5, (5, 4): 5, (3, 7): 6, (7, 3): 6
	, (2, 5): 1, (5, 2): 1, (2, 7): 3, (7, 2): 3, (5, 6): 2, (6, 5): 2
			  }
depot = 1
capacity = 7
minCost = [[0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 8, 4, 2, 7, 20, 10],
		   [0, 8, 0, 9, 6, 1, 14, 3],
		   [0, 4, 9, 0, 6, 10, 21, 6],
		   [0, 2, 6, 6, 0, 5, 18, 9],
		   [0, 7, 1, 10, 5, 0, 13, 4],
		   [0, 20, 14, 21, 18, 13, 0, 15],
		   [0, 10, 3, 6, 9, 4, 15, 0]]
costs = [[0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 8, 4, 2, 7, 20, 10],
		 [0, 8, 0, 9, 6, 1, 14, 3],
		 [0, 4, 9, 0, 6, 10, 21, 6],
		 [0, 2, 6, 6, 0, 5, 18, 9],
		 [0, 7, 1, 10, 5, 0, 13, 4],
		 [0, 20, 14, 21, 18, 13, 0, 15],
		 [0, 10, 3, 6, 9, 4, 15, 0]]
IFINITY = 100000


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


def floyd( martix ):
	nodeNum = len(martix[0])-1
	arr = []
	for j in range(1, nodeNum + 1):
		arr.clear()
		for l in range(1, nodeNum + 1):
			if martix[j][l] != 0:
				arr.append(l)
		for l in range(1, nodeNum + 1):
			if martix[l][j] != 0:
				for g in range(0, len(arr)):
					if martix[l][arr[g]] == 0:
						martix[l][arr[g]] = martix[l][j] + martix[j][arr[g]]
					else:
						if martix[l][arr[g]] > martix[l][j] + martix[j][arr[g]]:
							martix[l][arr[g]] = martix[l][j] + martix[j][arr[g]]
	for l in range(1, nodeNum + 1):
		martix[l][l] = 0



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
				R1loss.append((a, b))
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


floyd(costs)
print(costs)