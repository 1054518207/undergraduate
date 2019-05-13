# -*- coding: utf-8 -*-
"""
基于Pierre Dellacherie算法
@Author: lushaoxiao
@Date: 2019/5/12
@IDE: PyCharm
"""

GRID_NUM_WIDTH = 10
GRID_NUM_HEIGHT = 20


class AIWorker():
    SHAPES = ['L', 'J', 'S', 'Z', 'T', 'I', 'O']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]

    SHAPES_WITH_DIR = {
        'L': L, 'J': J, 'S': S, 'Z': Z, 'T': T, 'I': I, 'O': O
    }

    def __init__(self, center, shapeId, matrix):
        '''
        初始化
        :param center: [2,7] 选一个不会有任何碰撞的点
        :param shape: 'I', 'J', 'L', 'O', 'S', 'T', 'Z' 传递一个字母
        :param matrix: 当前矩阵
        '''
        self.center = center
        self.shape = self.SHAPES[shapeId]
        self.matrix = self.transfer_matrix(matrix)
        # station: 方块状态，为了数组不越界，默认设置为 0
        self.station = 0
        self.color = 1

    def transfer_matrix(self, matrix):
        newMatrix = []
        for line in matrix:
            lt = []
            for item in line:
                if item == 0:
                    lt.append(None)
                else:
                    lt.append(item)
            newMatrix.append(lt)
        return newMatrix

    def get_all_gridpos(self, center, shape, dir):
        curr_shape = self.SHAPES_WITH_DIR[shape][dir]

        return [(cube[0] + center[0], cube[1] + center[1])
                for cube in curr_shape]

    def conflict(self, center, matrix, shape, dir):
        for cube in self.get_all_gridpos(center, shape, dir):
            # 超出屏幕之外，说明不合法
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= GRID_NUM_HEIGHT or cube[1] >= GRID_NUM_WIDTH:
                return True

            screen_color_matrix = self.copyTheMatrix(matrix)
            # 不为None，说明之前已经有小方块存在了，也不合法
            if screen_color_matrix[cube[0]][cube[1]] is not None:
                return True

        return False

    def copyTheMatrix(self, screen_color_matrix):
        newMatrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        for i in range(len(screen_color_matrix)):
            for j in range(len(screen_color_matrix[i])):
                newMatrix[i][j] = screen_color_matrix[i][j]

        return newMatrix

    def getAllPossiblePos(self, thisShape='Z'):
        theMatrix = self.matrix
        theStationNum = len(self.SHAPES_WITH_DIR[thisShape])
        theResult = []
        for k in range(theStationNum):
            for j in range(len(theMatrix[1])):
                for i in range(len(theMatrix) - 1):
                    if self.conflict([i + 1, j], theMatrix, thisShape, k) == True and self.conflict([i, j], theMatrix,
                                                                                                    thisShape,
                                                                                                    k) == False:
                        if {"center": [i, j], "station": k} not in theResult:
                            theResult.append({"center": [i, j], "station": k})

        return theResult

    def getLandingHeight(self, center):
        return GRID_NUM_HEIGHT - 1 - center[0]

    def getErodedPieceCellsMetric(self, center, station):
        theNewMatrix = self.getNewMatrix(center, station)
        lines = 0
        usefulBlocks = 0
        theAllPos = self.get_all_gridpos(center, self.shape, station)
        for i in range(len(theNewMatrix) - 1, 0, -1):
            count = 0
            for j in range(len(theNewMatrix[1])):
                if theNewMatrix[i][j] is not None:
                    count += 1
            # 满一行
            if count == 15:
                lines += 1
                for k in range(len(theNewMatrix[1])):
                    if [i, k] in theAllPos:
                        usefulBlocks += 1
            # 整行未填充，则跳出循环
            if count == 0:
                break
        return lines * usefulBlocks

    def getNewMatrix(self, center, station):
        theNewMatrix = self.copyTheMatrix(self.matrix)
        theAllPos = self.get_all_gridpos(center, self.shape, station)
        for cube in theAllPos:
            theNewMatrix[cube[0]][cube[1]] = self.color
        return theNewMatrix

    def getBoardRowTransitions(self, theNewmatrix):
        transition = 0
        for i in range(len(theNewmatrix) - 1, 0, -1):
            count = 0
            for j in range(len(theNewmatrix[1]) - 1):
                if theNewmatrix[i][j] is not None:
                    count += 1
                if theNewmatrix[i][j] == None and theNewmatrix[i][j + 1] != None:
                    transition += 1
                if theNewmatrix[i][j] != None and theNewmatrix[i][j + 1] == None:
                    transition += 1
        return transition

    def getBoardColTransitions(self, theNewmatrix):
        transition = 0
        for j in range(len(theNewmatrix[1])):
            for i in range(len(theNewmatrix) - 1, 1, -1):
                if theNewmatrix[i][j] == None and theNewmatrix[i - 1][j] != None:
                    transition += 1
                if theNewmatrix[i][j] != None and theNewmatrix[i - 1][j] == None:
                    transition += 1
        return transition

    def getBoardBuriedHoles(self, theNewmatrix):
        holes = 0
        for j in range(len(theNewmatrix[1])):
            colHoles = None
            for i in range(len(theNewmatrix)):
                if colHoles == None and theNewmatrix[i][j] != None:
                    colHoles = 0

                if colHoles != None and theNewmatrix[i][j] == None:
                    colHoles += 1
            if colHoles is not None:
                holes += colHoles
        return holes

    def getBoardWells(self, theNewmatrix):
        sum_n = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
        wells = 0
        sum = 0

        for j in range(len(theNewmatrix[1])):
            for i in range(len(theNewmatrix)):
                if theNewmatrix[i][j] == None:
                    if (j - 1 < 0 or theNewmatrix[i][j - 1] != None) and (
                            j + 1 >= 10 or theNewmatrix[i][j + 1] != None):
                        wells += 1
                    else:
                        sum += sum_n[wells]
                        wells = 0
        return sum

    def mainProcess(self):
        '''
        主函数
        :return: 得到最优点坐标，包括形态
        '''
        pos = self.getAllPossiblePos(self.shape)
        bestScore = -999999  # 估值数字
        bestPoint = None  # 最优值点坐标
        for point in pos:
            theScore = self.evaluateFunction(point)
            if theScore > bestScore:
                bestScore = theScore
                bestPoint = point
            elif theScore == bestScore:
                if self.getPrioritySelection(point) < self.getPrioritySelection(bestPoint):
                    bestScore = theScore
                    bestPoint = point

        return bestPoint

    def getPrioritySelection(self, point):
        '''
        估值数字相同，按照路径长短以及形状变换获取优先级
        :param point: bestPoint坐标
        :return: 优先级
        '''
        tarStation = point['station']
        nowStation = self.station
        colNum = abs(7 - point['center'][1])
        if tarStation >= nowStation:
            changeTimes = tarStation - nowStation
        else:
            changeTimes = len(self.SHAPES_WITH_DIR[self.shape]) - nowStation + tarStation

        result = colNum * 100 + changeTimes
        if point['center'][1] <= 7:
            result += 10
        return result

    def evaluateFunction(self, point):
        '''
        估值函数
        :param point: 当前点坐标
        :return: 当前坐标的估值
        '''
        newMatrix = self.getNewMatrix(point['center'], point['station'])
        lh = self.getLandingHeight(point['center'])
        epcm = self.getErodedPieceCellsMetric(point['center'], point['station'])
        brt = self.getBoardRowTransitions(newMatrix)
        bct = self.getBoardColTransitions(newMatrix)
        bbh = self.getBoardBuriedHoles(newMatrix)
        bw = self.getBoardWells(newMatrix)

        # 两个计算分数的式子，前者更优，后者是PD算法的原始设计
        score = -45 * lh + 34 * epcm - 32 * brt - 98 * bct - 79 * bbh - 34 * bw
        # score = -1*lh + epcm - brt - bct - 4*bbh - bw
        return score


if __name__ == '__main__':
    shapeId = 5
    matrix = [[None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, 1, 1, 1],
              [None, None, None, None, None, None, None, 1, 1, 1],
              [None, None, None, None, None, None, None, 1, 1, 1],
              [None, None, None, None, None, None, None, 1, 1, 1]]
    ai = AIWorker([2, 7], shapeId, matrix)
    bestPoint = ai.mainProcess()
    station = bestPoint['station']
    center = bestPoint['center']
    print("shape:{};station:{};center:{}".format(shapeId, station, center))
