import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
level = 3




class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()
        chessboard = chessboard.tolist()
        ###build up neighbors
        neighbors = self.generate(chessboard)
        if self.color==1:
            unactor = -1
        else:
            unactor = 1
        if(len(neighbors)==0):
            # self.candidate_list.appemd((random.randint(0,self.chessboard_size-1),random.randint(0,self.chessboard_size-1)))
            self.candidate_list.append((10,10))
            return

        t = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        my_points = t.tolist()
        my_max = []
        q = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        his_points = q.tolist()
        his_max = []

        ###calculate all values
        while(len(neighbors)>0):
            x,y = neighbors.pop()

            chessboard[x][y]=self.color
            mypoint = self.calculate_person(chessboard,x,y,self.color)
            print(x,y,mypoint)
            my_points[x][y] = mypoint
            if len(my_max)>=1:
                a,b = my_max[0]
                if mypoint>my_points[a][b]:
                    my_max = [(x,y)]
                elif mypoint == my_points[a][b]:
                    my_max.append((x,y))
            else:
                my_max.append((x, y))

            chessboard[x][y] = unactor
            hispoint = self.calculate_person(chessboard,x,y,unactor)
            his_points[x][y] = hispoint
            print("his",x,y,hispoint)
            if len(his_max)>=1:
                a, b = his_max[0]
                if hispoint > his_points[a][b]:
                    his_max = [(x, y)]
                elif hispoint == his_points[a][b]:
                    his_max.append((x, y))
            else:
                his_max.append((x,y))

            chessboard[x][y]=0

        # get which one to next
        my_x,my_y = my_max[0]
        his_x,his_y = his_max[0]
        if self.color == 1:
            if my_points[my_x][my_y]>=his_points[his_x][his_y]:
                # if(my_points[my_x][my_y]>=900):
                #     if(len(my_max)>1):
                #         x, y = my_max.pop()
                #         point2 = his_points[x][y]
                #         while(len(my_max)>0):
                #             x1,y1 = my_max.pop()
                #             if(his_points[x1][y1]<point2):
                #                 x=x1
                #                 y=y1
                #     else:
                #         x,y = my_max.pop()
                #     self.candidate_list.append((x,y))
                # else:
                #     if (len(his_max) > 1):
                #         x, y = his_max.pop()
                #         point2 = my_points[x][y]
                #         while (len(his_max) > 0):
                #             x1, y1 = his_max.pop()
                #             if (my_points[x1][y1] > point2):
                #                 x = x1
                #                 y = y1
                #     else:
                #         x, y = his_max.pop()
                #     self.candidate_list.append((x, y))

                if (len(my_max) > 1):
                    x, y = my_max.pop()
                    point2 = his_points[x][y]
                    while (len(my_max) > 0):
                        x1, y1 = my_max.pop()
                        if (his_points[x1][y1] > point2):
                            x = x1
                            y = y1
                else:
                    x, y = my_max.pop()
                self.candidate_list.append((x, y))
            else:
                if (len(his_max) > 1):
                    x, y = his_max.pop()
                    point2 = my_points[x][y]
                    while (len(his_max) > 0):
                        x1, y1 = his_max.pop()
                        if (my_points[x1][y1] > point2):
                            x = x1
                            y = y1
                else:
                    x, y = his_max.pop()
                self.candidate_list.append((x, y))
        else:
            if my_points[my_x][my_y] >= his_points[his_x][his_y]:
                if (len(my_max) > 1):
                    x, y = my_max.pop()
                    point2 = his_points[x][y]
                    while (len(my_max) > 0):
                        x1, y1 = my_max.pop()
                        if (his_points[x1][y1] > point2):
                            x = x1
                            y = y1
                else:
                    x, y = my_max.pop()
                self.candidate_list.append((x, y))
            else:
                # if(his_points[his_x][his_y]>=1000):
                if (len(his_max) > 1):
                    x, y = his_max.pop()
                    point2 = my_points[x][y]
                    while (len(his_max) > 0):
                        x1, y1 = his_max.pop()
                        if (my_points[x1][y1] > point2):
                            x = x1
                            y = y1
                else:
                    x, y = his_max.pop()
                self.candidate_list.append((x, y))
                # else:
                #     if (len(my_max) > 1):
                #         x, y = my_max.pop()
                #         point2 = his_points[x][y]
                #         while (len(my_max) > 0):
                #             x1, y1 = my_max.pop()
                #             if (his_points[x1][y1] < point2):
                #                 x = x1
                #                 y = y1
                #     else:
                #         x, y = my_max.pop()
                #     self.candidate_list.append((x, y))
    ###function to generate neighbors
    def generate(self, chessboard):
        neighbor = set()
        for x in range(self.chessboard_size):
            for y in range(self.chessboard_size):
                if(chessboard[x][y]!=0):
                    if self.valid(x - 1, y, chessboard):
                        neighbor.add((x-1,y))
                    if self.valid(x + 1, y, chessboard):
                        neighbor.add((x+1,y))
                    if self.valid(x, y - 1, chessboard):
                        neighbor.add((x,y-1))
                    if self.valid(x, y + 1, chessboard):
                        neighbor.add((x,y+1))
                    if self.valid(x - 2, y, chessboard):
                        neighbor.add((x-2,y))
                    if self.valid(x, y - 2, chessboard):
                        neighbor.add((x,y-2))
                    if self.valid(x + 2, y, chessboard):
                        neighbor.add((x+2,y))
                    if self.valid(x, y + 2, chessboard):
                        neighbor.add((x,y+2))
                    if self.valid(x - 1, y + 1, chessboard):
                        neighbor.add((x-1,y+1))
                    if self.valid(x + 1, y + 1, chessboard):
                        neighbor.add((x+1,y+1))
                    if self.valid(x + 1, y - 1, chessboard):
                        neighbor.add((x+1,y-1))
                    if self.valid(x - 1, y - 1, chessboard):
                        neighbor.add((x-1,y-1))
                    if self.valid(x - 2, y + 2, chessboard):
                        neighbor.add((x-2,y+2))
                    if self.valid(x + 2, y + 2, chessboard):
                        neighbor.add((x+2,y+2))
                    if self.valid(x + 2, y - 2, chessboard):
                        neighbor.add((x+2,y-2))
                    if self.valid(x - 2, y - 2, chessboard):
                        neighbor.add((x-2,y-2))
        return neighbor

    def valid(self, x, y, chessboard):
        if (0 <= x < self.chessboard_size) & (0 <= y < self.chessboard_size) :
            if((chessboard[x][y] == 0)):
                return True
            return False

    ###function to evaluate current chessboard


    def calculate_person2(self, chessboard, i,j ,actor):

        total = 0
        if actor ==1:
            unactor = -1
        else:
            unactor = 1
        all_directions = self.Slice(chessboard,i,j,actor)
        # print(i,j)
        # print(np.array(all_directions))
        result = {'win5':0,'alive4':0,'die4':0,'lowdie4':0,'alive3':0,'tiao3':0,'die3':0,'alive2':0,'lowalive2':0,'die2':0,'notthreat':0}
        for x in range(4):
            line = all_directions[x]
            num=1
            left=-1
            right=-1
            for q in range(1, 5):
                flag = False
                if(left==-1):
                    if (line[4 - q] == line[4]):
                        num += 1
                        flag = True
                    else:
                        left = 4-q+1
                if(right==-1):
                    if (line[4 + q] == line[4]):
                        num += 1
                        flag = True
                    else:
                        right = 4+q-1

                if (not flag):
                    break;

            # print(line)
            if(left-1>=0):
                colorleft = line[left-1]
            else:
                colorleft = unactor

            if(right+1<9):
                colorright = line[right+1]
            else:
                colorright = unactor

            if(left-2>=0):
                colorleft1 = line[left-2]
            else:
                colorleft1 = unactor

            if (right + 2 < 9):
                colorright1 = line[right + 2]
            else:
                colorright1 = unactor

            if (left - 3 >= 0):
                colorleft2 = line[left - 3]
            else:
                colorleft2 = unactor

            if (right + 3 < 9):
                colorright2 = line[right + 3]
            else:
                colorright2 = unactor

            if(left - 4>=0):
                colorleft3 = line[left-4]
            else:
                colorleft3 = unactor

            if(right+4<9):
                colorright3 = line[right+4]
            else:
                colorright3 = unactor
            if i == 9 and j == 7 and actor==-1:
                print('here')
            if(num>=5):
                result['win5']+=1
            if(num==4):
                if(colorleft == 0 and colorright == 0):
                    result['alive4']+=1
                elif(colorleft == unactor) and (colorright == unactor ):
                    result['notthreat']+=1
                elif(colorleft == 0 or colorright == 0 ):
                    result['die4']+=1
            if num==3:
                if colorleft == 0 and colorright == 0 :
                    if colorleft1 == unactor and colorright1 == unactor:
                        result['die3']+=1
                    elif colorleft1 == actor or colorright1 == actor:
                        result['lowdie4']+=1
                    elif colorleft1 == 0 or colorright1 == 0:
                        result['alive3']+=1
                elif (colorleft == unactor) and (colorright == unactor):
                    result['notthreat']+=1
                elif (colorleft==0 or colorright ==0):
                    if(colorleft == unactor):
                        if(colorright1 == unactor):
                            result['notthreat']+=1
                        if(colorright1 == 0):
                            result['die3'] += 1
                        if(colorright1 == actor):
                            result['lowdie4']+=1
                    if(colorright == unactor):
                        if(colorleft1==unactor):
                            result['notthreat']+=1
                        if(colorleft1 == 0):
                            result['die3']+=1
                        if(colorleft1 == actor):
                            result['lowdie4']+=1
            if num==2:
                if (colorleft == 0 and colorright == 0):

                    if ((colorright1 == 0 and colorright2 == actor) or
                        (colorleft1 == 0 and colorleft2 == actor)):
                        result['die3']+=1 ### 死3
                    elif (colorleft1 == 0 and colorright1 == 0):
                         result['alive2']+=1 ### 活2

                    if ((colorright1 == actor and colorright2 == unactor) or
                            (colorleft1 == actor and colorleft2 == unactor)):
                         result['die3']+=1 ### 死3

                    if ((colorright1 == actor and colorright2 == actor) or
                            (colorleft1 == actor and colorleft2 == actor)):
                         result['lowdie4']+=1 ### 死4

                    if ((colorright1 == actor and colorright2 == 0) or
                            (colorleft1 == actor and colorleft2 == 0)):
                         result['tiao3']+=1 ### 跳活3


                elif (colorleft == unactor and colorright == unactor):
                     result['notthreat']+=1
                elif (colorleft == 0 or colorright == 0):

                    if (colorleft == unactor):
                        if (colorright1 == unactor or colorright2 == unactor) :
                             result['notthreat']+=1

                        elif (colorright1 == 0 and colorright2 == 0):### 均空
                            result['die2']+=1 ### 死2

                        elif (colorright1 == actor and colorright2 == actor): ### 均为自己的棋子
                            result['lowdie4']+=1 ### 死4

                        elif (colorright1 == actor or colorright2 == actor) :### 只有一个自己的棋子
                            result['die3']+=1 ### 死3

                    if (colorright == unactor) :### 右边被对方堵住
                        if (colorleft1 == unactor or colorleft2 == unactor): ### 只要有对方的一个棋子
                            result['notthreat']+=1 ### 没有威胁
                        elif (colorleft1 == 0 and colorleft2 == 0):### 均空
                             result['die2']+=1 ### 死2

                        elif (colorleft1 == actor and colorleft2 == actor):### 均为自己的棋子
                             result['lowdie4']+=1 ### 死4

                        elif (colorleft1 == actor or colorleft2 == actor) :### 只有一个自己的棋子
                             result['die3']+=1 ### 死3

            if (num == 1): ## 中心线1连


                if (colorleft == 0 and colorleft1 == actor and
                colorleft2 == actor and colorleft3 == actor):
                    result['lowdie4']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == actor):
                    result['lowdie4']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == actor and colorleft3 == 0 and colorright == 0):
                    result['tiao3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == 0 and colorleft == 0):
                    result['tiao3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == actor and colorleft3 == unactor and colorright == 0):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == unactor and colorleft == 0):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == 0 and
                        colorleft2 == actor and colorleft3 == actor):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == 0 and
                        colorright2 == actor and colorright3 == actor):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == 0 and colorleft3 == actor):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == 0 and colorright3 == actor):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == 0 and colorleft3 == 0 and colorright == 0):
                    result['lowalive2']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == 0 and colorright3 == 0 and colorleft == 0):
                    result['lowalive2']+=1

                if (colorleft == 0 and colorleft1 == 0 and
                        colorleft2 == actor and colorleft3 == 0 and colorright == 0):
                    result['lowalive2']+=1
                if (colorright == 0 and colorright1 == 0 and
                        colorright2 == actor and colorright3 == 0 and colorleft == 0):
                    result['lowalive2']+=1

        ## 其余在下边返回没有威胁
        if (result['win5'] >= 1):
            print(result)
            return 100000 ## 赢5
        if (result['alive4'] >=1 and result['alive3']>=1 ) or (result['alive4']>=1 and result['tiao3']>=1):
            return 12000
        if (result['alive4'] >= 1 ):
            return 11000
        if (result['die4'] >= 2 or (result['die4'] >= 1 and result['alive3'] >= 1) or (result['die4'] >= 1 and result['tiao3'] >= 1)
            ):
            return total if total>10000 else 10000
        if((result['lowdie4'] >= 1 and result['alive3'] >= 1) or (result['lowdie4'] >= 1 and result['tiao3'] >= 1)):
            return total if total>9000 else 9000
        if (result['alive3'] >= 2 or result['tiao3']>=2 or (result['alive3']>=1 and result['tiao3']>=1)):
            return  total if total>5000 else 5000

        # if result['die3']>=1 and result['alive3']>=1:
        #     return 2000

        # if (result['alive3'] >= 1):
        #     total += 1200
        #
        # if (result['die4'] >= 1):
        #     total += 1000
        #
        # if (result['tiao3'] >= 1):
        #     total += 800
        # if (result['lowdie4'] >= 1):
        #     total += 1000  ## 低级死4
        #
        # if (result['alive2'] >= 2):
        #     total += 400  ## 双活2
        # elif (result['alive2'] >= 1):
        #     total += 20  ## 活2
        #
        # if (result['lowalive2'] >= 1):
        #     total += 9  ## 低级活2
        #
        # if (result['die3'] >= 1):
        #     total += 3  ## 死3
        #
        # if (result['die2'] >= 1):
        #     total += 2  ## 死2

        return total

    def calculate_person(self, chessboard, i,j ,actor):

        total = 0
        if actor ==1:
            unactor = -1
        else:
            unactor = 1
        all_directions = self.Slice(chessboard,i,j,actor)
        # print(i,j)
        # print(np.array(all_directions))
        result = {'win5':0,'alive4':0,'die4':0,'lowdie4':0,'alive3':0,'tiao3':0,'die3':0,'alive2':0,'lowalive2':0,'die2':0,'notthreat':0}
        for x in range(4):
            line = all_directions[x]
            num=1
            left=-1
            right=-1
            for q in range(1, 5):
                flag = False
                if(left==-1):
                    if (line[4 - q] == line[4]):
                        num += 1
                        flag = True
                    else:
                        left = 4-q+1
                if(right==-1):
                    if (line[4 + q] == line[4]):
                        num += 1
                        flag = True
                    else:
                        right = 4+q-1

                if (not flag):
                    break;

            # print(line)
            if(left-1>=0):
                colorleft = line[left-1]
            else:
                colorleft = unactor

            if(right+1<9):
                colorright = line[right+1]
            else:
                colorright = unactor

            if(left-2>=0):
                colorleft1 = line[left-2]
            else:
                colorleft1 = unactor

            if (right + 2 < 9):
                colorright1 = line[right + 2]
            else:
                colorright1 = unactor

            if (left - 3 >= 0):
                colorleft2 = line[left - 3]
            else:
                colorleft2 = unactor

            if (right + 3 < 9):
                colorright2 = line[right + 3]
            else:
                colorright2 = unactor

            if(left - 4>=0):
                colorleft3 = line[left-4]
            else:
                colorleft3 = unactor

            if(right+4<9):
                colorright3 = line[right+4]
            else:
                colorright3 = unactor
            if i == 9 and j == 7 and actor==-1:
                print('here')
            if(num>=5):
                result['win5']+=1
            if(num==4):
                if(colorleft == 0 and colorright == 0):
                    result['alive4']+=1
                elif(colorleft == unactor) and (colorright == unactor ):
                    result['notthreat']+=1
                elif(colorleft == 0 or colorright == 0 ):
                    result['die4']+=1
            if num==3:
                if colorleft == 0 and colorright == 0 :
                    if colorleft1 == unactor and colorright1 == unactor:
                        result['die3']+=1
                    elif colorleft1 == actor or colorright1 == actor:
                        result['lowdie4']+=1
                    elif colorleft1 == 0 or colorright1 == 0:
                        result['alive3']+=1
                elif (colorleft == unactor) and (colorright == unactor):
                    result['notthreat']+=1
                elif (colorleft==0 or colorright ==0):
                    if(colorleft == unactor):
                        if(colorright1 == unactor):
                            result['notthreat']+=1
                        if(colorright1 == 0):
                            result['die3'] += 1
                        if(colorright1 == actor):
                            result['lowdie4']+=1
                    if(colorright == unactor):
                        if(colorleft1==unactor):
                            result['notthreat']+=1
                        if(colorleft1 == 0):
                            result['die3']+=1
                        if(colorleft1 == actor):
                            result['lowdie4']+=1
            if num==2:
                if (colorleft == 0 and colorright == 0):

                    if ((colorright1 == 0 and colorright2 == actor) or
                        (colorleft1 == 0 and colorleft2 == actor)):
                        result['die3']+=1 ### 死3
                    elif (colorleft1 == 0 and colorright1 == 0):
                         result['alive2']+=1 ### 活2

                    if ((colorright1 == actor and colorright2 == unactor) or
                            (colorleft1 == actor and colorleft2 == unactor)):
                         result['die3']+=1 ### 死3

                    if ((colorright1 == actor and colorright2 == actor) or
                            (colorleft1 == actor and colorleft2 == actor)):
                         result['lowdie4']+=1 ### 死4

                    if ((colorright1 == actor and colorright2 == 0) or
                            (colorleft1 == actor and colorleft2 == 0)):
                         result['tiao3']+=1 ### 跳活3


                elif (colorleft == unactor and colorright == unactor):
                     result['notthreat']+=1
                elif (colorleft == 0 or colorright == 0):

                    if (colorleft == unactor):
                        if (colorright1 == unactor or colorright2 == unactor) :
                             result['notthreat']+=1

                        elif (colorright1 == 0 and colorright2 == 0):### 均空
                            result['die2']+=1 ### 死2

                        elif (colorright1 == actor and colorright2 == actor): ### 均为自己的棋子
                            result['lowdie4']+=1 ### 死4

                        elif (colorright1 == actor or colorright2 == actor) :### 只有一个自己的棋子
                            result['die3']+=1 ### 死3

                    if (colorright == unactor) :### 右边被对方堵住
                        if (colorleft1 == unactor or colorleft2 == unactor): ### 只要有对方的一个棋子
                            result['notthreat']+=1 ### 没有威胁
                        elif (colorleft1 == 0 and colorleft2 == 0):### 均空
                             result['die2']+=1 ### 死2

                        elif (colorleft1 == actor and colorleft2 == actor):### 均为自己的棋子
                             result['lowdie4']+=1 ### 死4

                        elif (colorleft1 == actor or colorleft2 == actor) :### 只有一个自己的棋子
                             result['die3']+=1 ### 死3

            if (num == 1): ## 中心线1连
                if (colorleft == 0 and colorleft1 == actor and
                colorleft2 == actor and colorleft3 == actor):
                    result['lowdie4']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == actor):
                    result['lowdie4']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == actor and colorleft3 == 0 and colorright == 0):
                    result['tiao3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == 0 and colorleft == 0):
                    result['tiao3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == actor and colorleft3 == unactor and colorright == 0):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == actor and colorright3 == unactor and colorleft == 0):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == 0 and
                        colorleft2 == actor and colorleft3 == actor):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == 0 and
                        colorright2 == actor and colorright3 == actor):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == 0 and colorleft3 == actor):
                    result['die3']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == 0 and colorright3 == actor):
                    result['die3']+=1

                if (colorleft == 0 and colorleft1 == actor and
                        colorleft2 == 0 and colorleft3 == 0 and colorright == 0):
                    result['lowalive2']+=1
                if (colorright == 0 and colorright1 == actor and
                        colorright2 == 0 and colorright3 == 0 and colorleft == 0):
                    result['lowalive2']+=1

                if (colorleft == 0 and colorleft1 == 0 and
                        colorleft2 == actor and colorleft3 == 0 and colorright == 0):
                    result['lowalive2']+=1
                if (colorright == 0 and colorright1 == 0 and
                        colorright2 == actor and colorright3 == 0 and colorleft == 0):
                    result['lowalive2']+=1

        ## 其余在下边返回没有威胁
        print(result)

        if (1):
            print(result)
            return 100000 ## 赢5
        if (result['alive4'] >=1 and result['alive3']>=1 ) or (result['alive4']>=1 and result['tiao3']>=1):
            return 12000
        if (result['alive4'] >= 1 ):
            return 11000
        if (result['die4'] >= 2 or (result['die4'] >= 1 and result['alive3'] >= 1) or (result['die4'] >= 1 and result['tiao3'] >= 1)
            ):
            return total if total>10000 else 10000
        if((result['lowdie4'] >= 1 and result['alive3'] >= 1) or (result['lowdie4'] >= 1 and result['tiao3'] >= 1)):
            return total if total>9000 else 9000
        if (result['alive3'] >= 2 or result['tiao3']>=2 or (result['alive3']>=1 and result['tiao3']>=1)):
            return  total if total>5000 else 5000
        else:
            flag = 0
            for a in range(i-4 , i+5):
                for b in range(j-4,j+5):
                    if 0<=a<self.chessboard_size and 0<=b<self.chessboard_size :
                        if(chessboard[a][b] == actor):
                            grade = self.calculate_person2(chessboard,a,b,actor)
                            if grade>=total and grade >=5000 :
                                return grade
                            else:
                                total+=grade
                                flag=1
                                break
                if flag == 1:
                    break
        #
        # if result['die3']>=1 and result['alive3']>=1:
        #     return  total if total>2000 else 2000

        if (i == 5 and j == 9):
            print("aaa")
        # if (result['die4'] >= 1):
        #     total+= 1000
        # if (result['lowdie4'] >= 1):
        #     total+= 900  ## 低级死4
        #
        # if ( result['alive3'] >= 1):
        #     total+= 600
        #
        # if (result['tiao3'] >= 1):
        #     total+= 500
        #
        #
        # if (result['alive2'] >= 1):
        #     total+= result['alive2']*20  ## 活2
        #
        # if (result['lowalive2'] >= 1):
        #     total+= result['lowalive2']*9 ## 低级活2
        #
        # if (result['die3'] >= 1):
        #     total+= result['die3']*3 ## 死3
        #
        # if (result['die2'] >= 1):
        #     total+= result['die2']*2 ## 死2
        if (result['alive3'] >= 1):
            if actor == self.color:
                total += 1500
            else:
                total+=900

        if (result['die4'] >= 1):
            if actor == self.color:
                total += 1000
            else:
                total+= 1400

        if (result['tiao3'] >= 1):
            if actor == self.color:
                total += 800
            else:
                total+= 30

        if (result['lowdie4'] >= 1):
            if actor == self.color:
                total += 900  ## 低级死4
            else:
                total+= 900

        if (result['alive2'] >= 2):
            if actor == self.color:
                total += 500  ## 双活2
            else:
                total+=20
        elif (result['alive2'] >= 1):
            if actor == self.color:
                total += 200  ## 活2
            else:
                total += 20

        if (result['lowalive2']>=2):
            total+= 380
        elif (result['lowalive2'] >= 1):
            total += 18  ## 低级活2

        if (result['die3'] >= 1):
            total += 3  ## 死3

        if (result['die2'] >= 1):
            total += 2  ## 死2

        return total

    def Slice(self,chessboard,i,j,actor):
        all_directions = [[],[],[],[]]
        if actor==1:
            unactor = -1
        else:
            unactor = 1

        for q in range(-4,5):
            if(0<=j+q<self.chessboard_size):
                all_directions[0].append(chessboard[i][j+q])
            else:
                all_directions[0].append(unactor)

            if(0<=i+q<self.chessboard_size):
                all_directions[1].append(chessboard[i+q][j])
            else:
                all_directions[1].append(unactor)

            if(0<=j+q<self.chessboard_size and 0<=i+q<self.chessboard_size):
                all_directions[2].append(chessboard[i+q][j+q])
            else:
                all_directions[2].append(unactor)

            if(0<=j+q<self.chessboard_size and 0<=i-q<self.chessboard_size):
                all_directions[3].append(chessboard[i-q][j+q])
            else:
                all_directions[3].append(unactor)
        return all_directions





