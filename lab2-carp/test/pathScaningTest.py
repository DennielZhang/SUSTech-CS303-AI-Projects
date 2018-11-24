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
		 [0,0,8,4,2,7,20,10],
		 [0,8,0,9,6,1,14,3],
		 [0,4,9,0,6,10,21,6],
		 [0,2,6,6,0,5,18,9],
		 [0,7,1,10,5,0,13,4],
		 [0,20,14,21,18,13,0,15],
		 [0,10,3,6,9,4,15,0]]
IFINITY = 100000

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

print(pathScaning(5))