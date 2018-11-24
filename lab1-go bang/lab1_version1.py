import numpy as np
import random 
import time 

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
level = 3


class node: 
    def _init_ (self,x,y,i,inneighbors = False):
        self.x = x
        self.y = y
        self.i = i
        self.value = 0
        self.inneighbors = inneighbors
    def set_value(self,a):
        self.value = a 
class AI(object):
    def _init_(self, chessboard_size , color , time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
    
    def go(self,chessboard):
        self.candidate_list.clear()
        
        chessboard_copy1 = chessboard.copy()
        chessboard_copy2 = []
        ###get formal chessboard value
        max_value = self.evaluate(chessboard)

        ###build up neighbors
        neighbors = self.generate(chessboard)

        ###define the stack to contain first step chess
        first_step = []
        ###start dfs
        while len(neighbors)!=0 :
            n = neighbors.pop()
            if(n.i == 1):
                ###when meet the first level item , we need to refresh the chessboard to the start time
                chessboard = chessboard_copy1.copy()
                first_step.append((n.x,n.y))###special for first step

                chessboard[n.x][n.y] = self.color

                ###prepare copy for next level
                chessboard_copy2 = chessboard.copy()
                self.add_neighbor(n.x,n.y,2,chessboard,neighbors)
                value = self.evaluate(chessboard)
                if(value>max_value):
                    self.candidate_list.append(first_step[-1])
            if(n.i==2):
                ###when meet the second level item , we need to refresh the chessboard to the nearst chessboard after 
                ###corresponding first step
                chessboard = chessboard_copy2.copy()
                chessboard[n.x][n.y] = -1 if self.color==1 else 1
                self.add_neighbor(n.x,n.y,3,chessboard,neighbors)
                value = self.evaluate(chessboard)
                if(value>max_value):
                    self.candidate_list.append(first_step[-1])
            if (n.i==3):
                ###when meet the third level item , we don't need to refresh the chessboard but we need to delete 
                ###the chess later
                chessboard[n.x][n.y] = self.color
                value = self.evaluate(chessboard)
                if(value>max_value):
                    self.candidate_list.append(first_step[-1])
                chessboard[n.x][n.y] = 0

    ###function to add neighbors according to one node
    def add_neighbor(self,x,y,i,chessboard,neighbors):
        if self.valid2( node(x-1,y,i,True),chessboard,neighbors):
            a = node(x-1,y,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+1,y,i,True),chessboard,neighbors):
            a = node(x+1,y,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x,y-1,i,True),chessboard,neighbors):
            a = node(x,y-1,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x,y+1,i,True),chessboard,neighbors):
            a = node(x,y+i,True)
            neighbors.ppend(a)
        if self.valid2( node(x-2,y,i,True),chessboard,neighbors):
            a = node(x-2,y,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x,y-2,i,True),chessboard,neighbors):
            a = node(x,y-2,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+2,y,i,True),chessboard,neighbors):
            a = node(x+2,y,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x,y+2,i,True),chessboard,neighbors):
            a = node(x,y+2,True)
            neighbors.ppend(a)
        if self.valid2( node(x-1,y+1,i,True),chessboard,neighbors):
            a = node(x-1,y+1,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+1,y+1,i,True),chessboard,neighbors):
            a = node(x+1,y+1,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+1,y-1,i,True),chessboard,neighbors):
            a = node(x+1,y-1,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x-1,y-1,i,True),chessboard,neighbors):
            a = node(x-1,y-1,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x-2,y+2,i,True),chessboard,neighbors):
            a = node(x-2,y+2,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+2,y+2,i,True),chessboard,neighbors):
            a = node(x+2,y+2,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x+2,y-2,i,True),chessboard,neighbors):
            a = node(x+2,y-2,i,True)
            neighbors.ppend(a)
        if self.valid2( node(x-2,y-2,i,True),chessboard,neighbors):
            a = node(x-2,y-2,i,True)
            neighbors.ppend(a)
    ###function to generate neighbors                            
    def generate(self,chessboard):
        neighbor = []
        for x in range(self.chessboard_size):
            for y in range(self.chessboard_size):
                if self.valid(x-1,y,chessboard):
                    a = node(x-1,y,1,True)
                    neighbor.append(a)
                if self.valid(x+1,y,chessboard):
                    a = node(x+1,y,1,True)
                    neighbor.append(a)
                if self.valid(x,y-1,chessboard):
                    a = node(x,y-1,1,True)
                    neighbor.append(a)
                if self.valid(x,y+1,chessboard):
                    a = node(x,y+1,True)
                    neighbor.append(a)
                if self.valid(x-2,y,chessboard):
                    a = node(x-2,y,1,True)
                    neighbor.append(a)
                if self.valid(x,y-2,chessboard):
                    a = node(x,y-2,1,True)
                    neighbor.append(a)
                if self.valid(x+2,y,chessboard):
                    a = node(x+2,y,1,True)
                    neighbor.append(a)
                if self.valid(x,y+2,chessboard):
                    a = node(x,y,y+2,True)
                    neighbor.append(a)
                if self.valid(x-1,y+1,chessboard):
                    a = node(x-1,y+1,1,True)
                    neighbor.append(a)
                if self.valid(x+1,y+1,chessboard):
                    a = node(x+1,y+1,1,True)
                    neighbor.append(a)
                if self.valid(x+1,y-1,chessboard):
                    a = node(x+1,y-1,1,True)
                    neighbor.append(a)
                if self.valid(x-1,y-1,chessboard):
                    a = node(x-1,y-1,1,True)
                    neighbor.append(a)
                if self.valid(x-2,y+2,chessboard):
                    a = node(x-2,y+2,1,True)
                    neighbor.append(a)
                if self.valid(x+2,y+2,chessboard):
                    a = node(x+2,y+2,1,True)
                    neighbor.append(a)
                if self.valid(x+2,y-2,chessboard):
                    a = node(x+2,y-2,1,True)
                    neighbor.append(a)
                if self.valid(x-2,y-2,chessboard):
                    a = node(x-2,y-2,1,True)
                    neighbor.append(a)
        return neighbor
    def valid(self,x,y,chessboard):
        if 0<=x<=14&0<=y<14&chessboard[x][y]==COLOR_NONE:
            return True
        else:
            return False
    def valid2(self,node,chessboard,neighbors):
        if 0<=node.x<=14&0<=node.y<14&chessboard[node.x][node.y]==COLOR_NONE&(node not in neighbors):
            return True
        else:
            return False
    ###function to evaluate current chessboard
    def evaluate(self,chessboard):
        computer_credit = self.calculate_person(chessboard,self.color)
        person_credit = self.calculate_person(chessboard,-1 if self.color==1 else 1)
        return computer_credit-person_credit
        
    def calculate_person(self,chessboard,actor):
        total = 0
        if actor == 1:
            unactor = -1
        else:
            unactor = 1
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                s = self.chessboard_size
                if chessboard[i][j] == 0:
                    ###判断双冲四
                    if(j+3<s and i+3<s ):
                        if(chessboard[i][j+1]==actor and chessboard[i][j+2] == actor and chessboard[i][j+3]==actor
                        and chessboard[i+1][j+1]==actor and chessboard[i+2][j+2] == actor and chessboard[i+3][j+3] == actor):
                            if(j-1>=0 and chessboard[i][j-1]!=unactor)and(i-1>=0 and chessboard[i-1][j-1]!=unactor):
                                total+=10000
                            elif(j+4<s and chessboard[i][j+4]!=unactor)and(i+4<s and chessboard[i+4][j+4]!=unactor):
                                total+=10000
                        elif (chessboard[i][j+1]==actor and chessboard[i][j+2] == actor and chessboard[i][j+3]==actor
                        and chessboard[i+1][j]==actor and chessboard[i+2][j] == actor and chessboard[i+3][j] == actor):
                            if(j-1>=0 and chessboard[i][j-1]!=unactor)and(i-1>=0 and chessboard[i-1][j]!=unactor):
                                total+=10000
                            elif(j+4<s and chessboard[i][j+4]!=unactor)and(i+4<s and chessboard[i+4][j]!=unactor):
                                total+=10000
                        elif (chessboard[i+1][j+1]==actor and chessboard[i+2][j+2] == actor and chessboard[i+3][j+3]==actor
                        and chessboard[i+1][j]==actor and chessboard[i+2][j] == actor and chessboard[i+3][j] == actor):
                            if (j - 1 >= 0 and chessboard[i-1][j - 1] != unactor) and (
                                    i - 1 >= 0 and chessboard[i - 1][j] != unactor):
                                total += 10000
                            elif (j + 4 < s and chessboard[i+4][j + 4] != unactor) and (
                                    i + 4 < s and chessboard[i + 4][j] != unactor):
                                total += 10000
                    if(j-3>0 and i+3<s):
                        if (chessboard[i+1][j+1] == actor and chessboard[i+2][j+2] == actor and chessboard[i+3][j+3] == actor
                            and chessboard[i+1][j-1] == actor and chessboard[i+2][j-2] == actor and chessboard[i+3][j-3] == actor):
                            if (i - 1 >= 0 and chessboard[i-1 ][j -1] != unactor) and (
                                    j+1 <s and chessboard[i - 1][j+1] != unactor):
                                total += 10000
                            elif (j + 4 < s and j-4>0 and chessboard[i+4][j + 4] != unactor) and (
                                    i + 4 < s and chessboard[i + 4][j-4] != unactor):
                                total += 10000
                        if (chessboard[i+1][j] == actor and chessboard[i+2][j] == actor and chessboard[i+3][j] == actor
                            and chessboard[i+1][j-1] == actor and chessboard[i+2][j-2] == actor and chessboard[i+3][j-3] == actor):
                            if (j +1<s and chessboard[i-1][j+1] != unactor) and (
                                    i - 1 >= 0 and chessboard[i - 1][j] != unactor):
                                total += 10000
                            elif (i + 4 < s and chessboard[i+4][j] != unactor) and (
                                    j - 4 >0 and chessboard[i + 4][j-4] != unactor):
                                total += 10000
                    ###判断双活三
                    if (j + 3 < s and i + 3 < s and i-1>0 and j-1>0):
                        if (chessboard[i][j + 1] == actor and chessboard[i][j + 2] == actor
                                and chessboard[i + 1][j + 1] == actor and chessboard[i + 2][j + 2] == actor ):
                            if(chessboard[i-1][j-1]!=unactor and chessboard[i][j-1]!=unactor and chessboard[i+3][j+3]!=unactor and chessboard[i][j+3]!=unactor):
                                total += 10000
                        elif (chessboard[i][j + 1] == actor and chessboard[i][j + 2] == actor
                              and chessboard[i + 1][j] == actor and chessboard[i + 2][j] == actor ):
                            if (chessboard[i - 1][j ] != unactor and chessboard[i][j - 1] != unactor and
                                    chessboard[i + 3][j ] != unactor and chessboard[i][j + 3] != unactor):
                                total += 10000
                        elif (chessboard[i + 1][j + 1] == actor and chessboard[i + 2][j + 2] == actor
                              and chessboard[i+1][j]==actor and chessboard[i+2][j] == actor):
                            if (chessboard[i - 1][j - 1] != unactor and chessboard[i-1][j] != unactor and
                                    chessboard[i + 3][j + 3] != unactor and chessboard[i+3][j] != unactor):
                                total += 10000
                    if (j - 3>= 0 and i + 3 < s and i-1>=0 and j+3<s):
                        if (chessboard[i + 1][j + 1] == actor and chessboard[i + 2][j + 2] == actor
                                and chessboard[i + 1][j - 1] == actor and chessboard[i + 2][j - 2] == actor ):
                            if (chessboard[i - 1][j - 1] != unactor and chessboard[i-1][j + 1] != unactor and
                                    chessboard[i + 3][j + 3] != unactor and chessboard[i+3][j -3] != unactor):
                                total += 10000
                        if (chessboard[i + 1][j] == actor and chessboard[i + 2][j] == actor
                                and chessboard[i + 1][j - 1] == actor and chessboard[i + 2][j - 2] == actor ):
                            if (chessboard[i - 1][j] != unactor and chessboard[i-1][j - 1] != unactor and
                                    chessboard[i + 3][j] != unactor and chessboard[i+3][j-3] != unactor):
                                total += 10000
                if chessboard[i][j] ==1:
                    ###判断连五 +20000
                    if(j+4<s and chessboard[i][j+1]==actor and chessboard[i][j+2]==actor and chessboard[i][j+3]==actor and chessboard[i][j+4]==actor):
                        total+=200000
                        return total
                    if(i+4<s and j+4<s and chessboard[i+1][j+1]==actor and chessboard[i+2][j+2]==actor and chessboard[i+3][j+3]==actor and chessboard[i+4][j+4]==actor):
                        total+=200000
                        return total
                    if(i+4<s and chessboard[i+1][j]==actor and chessboard[i+2][j]==actor and chessboard[i+3][j]==actor and chessboard[i+4][j]==actor):
                        total+=200000
                        return total
                    if(j-4>=0 and i+4<s and chessboard[i+1][j-1]==actor and chessboard[i+2][j-2]==actor and chessboard[i+3][j-3]==actor and chessboard[i+4][j-4]==actor):
                        total+=200000
                        return total
                    ###判断活四 +10000 判断冲四 +10000
                    if (j + 3 < s  and chessboard[i][j + 1] == actor and chessboard[i][j + 2] == actor  and chessboard[i][j + 3] == actor ):
                        if(j - 1 >= 0 and j+4<s and chessboard[i][j - 1] != unactor and chessboard[i][j+4]!=unactor):
                            total += 200000
                            return total
                        else:
                            total += 10000
                    if ( i + 3 < s and j + 3 < s and chessboard[i + 1][j + 1] == actor and chessboard[i + 2][j + 2] == actor and chessboard[i + 3][j + 3] == actor ):
                        if(i-1>=0 and j-1>=0 and i + 4 < s and j + 4 < s and chessboard[i + 4][j + 4] != unactor and chessboard[i-1][j-1]!= unactor):
                            total += 200000
                            return total
                        else:
                            total+=10000
                    if (i+3<s and chessboard[i+1][j] == actor and chessboard[i+2][j] == actor  and chessboard[i+3][j] == actor ):
                        if(i-1 >=0 and chessboard[i-1][j]!=unactor and i + 4 < s and chessboard[i+4][j]!=unactor):
                            total += 200000
                            return total
                        else :
                            total+=10000
                    if (j - 3 >=0 and i + 3 < s  and chessboard[i +1][j - 1] == actor and chessboard[i + 2][
                        j - 2] == actor and chessboard[i+3][j - 3] == actor ):
                        if(j - 4 >=0 and i + 4 < s and j+1 < s and i-1>=0 and chessboard[i + 4][j - 4] != unactor and chessboard[i - 1][j + 1] != unactor):
                            total += 200000
                            return total
                        else:
                            total+=10000
                    ###判断连三 +10000 判断眠三 +4000
                    if (j + 2 < s  and chessboard[i][j + 1] == actor and chessboard[i][j + 2] == actor  ):
                        if(j - 1 >= 0 and j+3<s and chessboard[i][j - 1] != unactor and chessboard[i][j+3]!=unactor):
                            total += 10000
                        else:
                            total += 4000
                    if ( i + 2 < s and j + 2 < s and chessboard[i + 1][j + 1] == actor and chessboard[i + 2][j + 2] == actor  ):
                        if(i-1>=0 and j-1>=0 and i + 3 < s and j + 3 < s and chessboard[i + 3][j + 3] != unactor and chessboard[i-1][j-1]!= unactor):
                            total += 10000
                        else:
                            total+=4000
                    if (i+2<s and chessboard[i+1][j] == actor and chessboard[i+2][j] == actor  ):
                        if(i-1 >=0 and chessboard[i-1][j]!=unactor and i + 3 < s and chessboard[i+3][j]!=unactor):
                            total += 10000
                        else :
                            total+=4000
                    if (j - 2 >=0 and i + 2 < s  and chessboard[i +1][j - 1] == actor and chessboard[i + 2][
                        j - 2] == actor ):
                        if(j - 3 >=0 and i + 3 < s and j+1 < s and i-1>=0 and chessboard[i + 3][j - 3] != unactor and chessboard[i - 1][j + 1] != unactor):
                            total += 10000
                            return total
                        else:
                            total+=4000

                    ###判断跳三 +10000
                    if(j-1>=0 and j+4<s and chessboard[i][j+1]==actor and chessboard[i][j+3]==actor and chessboard[i][j+2]==0 and chessboard[i][j-1]!=unactor and chessboard[i][j+4]!=unactor)or(
                            j - 1 >=0 and j + 4 < s and chessboard[i][j+1] == 0 and chessboard[i][j + 2] == actor and chessboard[i][j + 3] == actor and chessboard[i][j - 1] != unactor and chessboard[i][j + 4] != unactor):
                        total+=10000
                    if(j-1>=0 and j+4<s and i-1>=0 and i+4<s and chessboard[i-1][j-1]==0 and  chessboard[i+1][j+1]==actor and chessboard[i+2][j+1]== 0  and chessboard[i+3][j+3]==actor and chessboard[i+4][j+4]!=unactor)or(
                            j-1>=0 and j+4<s and i-1>=0 and i+4<s and chessboard[i-1][j-1]==0 and chessboard[i+1][j+1]==0 and chessboard[i+2][j+1]== actor  and chessboard[i+3][j+3]==actor and chessboard[i+4][j+4]!=unactor):
                        total+=10000
                    if(i-1>=0 and i+4<s and chessboard[i-1][j]!=unactor and chessboard[i+1][j] ==actor and chessboard[i+2][j] == 0  and chessboard[i+3][j] == actor and chessboard[i+4][j]!=unactor) or(
                            i-1>=0 and i+4<s and chessboard[i-1][j]!=unactor and chessboard[i+1][j] ==0 and chessboard[i+2][j] == actor  and chessboard[i+3][j] == actor and chessboard[i+4][j]!=unactor):
                        total+=10000
                    if(j+1<s and i-1>=0 and j-4>=0 and i+4<s and chessboard[i-1][j+1]==unactor and chessboard[i+1][j-1]==actor and chessboard[i+2][j-2]==0 and chessboard[i+3][j-3]==actor and chessboard[i+4][j-4]!=unactor) or(
                            j+1<s and i-1>=0 and j-4>=0 and i+4<s and chessboard[i-1][j+1]==unactor and chessboard[i+1][j-1]==0 and chessboard[i+2][j-2]==actor and chessboard[i+3][j-3]==actor and chessboard[i+4][j-4]!=unactor):
                        total+=10000
                    ###判断活二 +1000 判断眠二 +500
                    if(j+1<s and chessboard[i][j+1]==actor):
                        if(j-1>=0 and j+2<s and chessboard[i][j-1]!=unactor and chessboard[i][j+2]!=unactor ):
                            total+=1000
                        else:
                            total+=500
                    if(i+1<s and j+1<s and chessboard[i+1][j+1]==actor ):
                        if(j-1>=0 and j+2<s and i-1>=0 and i+2<s and chessboard[i-1][j-1]!=unactor and chessboard[i+2][j+2]!=unactor):
                            total+=1000
                        else:
                            total+=500
                    if(i+1<s and chessboard[i+1][j]==actor):
                        if(i-1>=0 and i+2<s and chessboard[i-1][j]!=unactor and chessboard[i+2][j]!=unactor):
                            total+=1000
                        else:
                            total+=500
                    if(i+1<s and j-1>=0 and chessboard[i+1][j-1]==actor):
                        if(i-1>=0 and j+1<s and i+2<s and j-2>=0 and chessboard[i-1][j+1]!=unactor and chessboard[i+2][j-2]!=unactor):
                            total+=1000
                        else:
                            total+=500
                    #########.................
                    return total






