# -*- coding: utf-8 -*-
"""

Construct the board with a bound
							   y++
		 *							   ^
		 * 1 1 1 1 1 1 1 1 1 1 1 1  21 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  20 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  19 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  18 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  17 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  16 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  15 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  14 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  13 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  12 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  11 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  10 |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  9  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  8  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  7  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  6  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  5  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  4  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  3  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  2  |
		 * 1 0 0 0 0 0 0 0 0 0 0 1  1  |
		 * 1 1 1 1 1 1 1 1 1 1 1 1  0  |
		 *
		 * 1 1 9 8 7 6 5 4 3 2 1 0-----------> x--
		 * 1 0


@Author: lushaoxiao
@Date: 2019/5/6
@IDE: PyCharm
"""
import json


class Method(object):
    # 10列
    COLS = 10
    # 20行
    ROWS = 20
    SHAPES = ['L', 'J', 'S', 'Z', 'T', 'I', 'O']
    shapeL = {
        "shape0": [[1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 1, 1, 1]],
        "shape3": [[0, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]]
    }
    shapeJ = {
        "shape0": [[1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 1]],
        "shape3": [[0, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
    }
    shapeS = {
        "shape0": [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 1, 1, 0]],
        "shape3": [[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0]]
    }
    shapeZ = {
        "shape0": [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]],
        "shape3": [[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0]]
    }
    shapeT = {
        "shape0": [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1], [0, 0, 1, 0]],
        "shape3": [[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0]]
    }
    shapeI = {
        "shape0": [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]],
        "shape3": [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
    }
    shapeO = {
        "shape0": [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape1": [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        "shape2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        "shape3": [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]]
    }

    SHAPES_WITH_DETAIL = {
        'L': shapeL,
        'J': shapeJ,
        'S': shapeS,
        'Z': shapeZ,
        'T': shapeZ,
        'I': shapeI,
        'O': shapeO
    }

    def __init__(self, blockId, board):
        self._startx = 0
        self._starty = 9
        self.board = list(board)
        if 0 <= blockId < len(self.SHAPES):
            self.block = self.SHAPES_WITH_DETAIL[self.SHAPES[blockId]]['shape0']
        else:
            raise RuntimeError("blockId错误")

    def get_all_gridpos(self, block):
        '''
        得到当前方块所有的可放位置，位置坐标为二维列表
        :param block: 俄罗斯方块的形状
        :return: list
        '''
        lt = []
        block = self.cutBlock(block)
        for x in range(self.ROWS-1, -1, -1):
            for y in range(self.COLS):
                if self.board[x][y] == 0 and self.valid(x, y, block):
                    pos = [x, y]
                    lt.append(pos)
        return lt

    def valid(self, xPos, yPos, blockShape):
        '''
        判断所给方块坐标是否可行
        :param xPos: x轴位置
        :param yPos: y轴位置
        :param blockShape: 当前方块形状
        :return: 在此处放置是否合适
        '''
        for x in range(curRows - 1, -1, -1):
            for y in range(curCols):
                if blockShape[x][y] != 0:
                    try:
                        if 0 <= xPos + x and 0 <= yPos + y and self.board[xPos + x][yPos + y] != 0:
                            return False
                        else:
                            continue
                    except Exception:
                        return False
        return True

    # def hasBottom(self,xPos,yPos):
    #     block = self.cutBlock(self.block)
    #     for x in range(curRows):
    #         for y in range(curCols-1, -1, -1):
    #             if block[x][y] != 0
    #     return self.board[xPos][yPos+1] != 0

    def cutBlock(self, block):
        '''
        裁剪方块
        :param block: 原始方块
        :return: 裁剪好之后的方块
        '''
        newBlock = []
        cnt = 0
        global curRows
        global curCols
        for x in range(4):
            if block[x][0] == 0 and block[x][1] == 0 and block[x][2] == 0 and block[x][3] == 0:
                continue
            else:
                lt = [block[x][0], block[x][1], block[x][2], block[x][3]]
                newBlock.append(lt)
                cnt += 1
        fBlock = []
        ax = []
        ay = []
        az = []
        curRows = cnt
        if cnt == 2:
            for y in range(4):
                if newBlock[0][y] == 0 and newBlock[1][y] == 0:
                    continue
                else:
                    ax.append(newBlock[0][y])
                    ay.append(newBlock[1][y])
            fBlock = [ax, ay]
            curCols = 3
        elif cnt == 3:
            for y in range(4):
                if newBlock[0][y] == 0 and newBlock[1][y] == 0 and newBlock[2][y] == 0:
                    continue
                else:
                    ax.append(newBlock[0][y])
                    ay.append(newBlock[1][y])
                    az.append(newBlock[2][y])
            fBlock = [ax, ay, az]
            curCols = 2
        elif cnt == 4:
            fBlock = [[1], [1], [1], [1]]
            curCols = 1
        else:
            curCols = 4
            fBlock = newBlock
        return fBlock

    def getPos(self):
        data = {
            "x": self._startx,
            "y": self._starty
        }
        return json.dumps(data)


if __name__ == '__main__':
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    m = Method(blockId=5, board=board)
    lt = m.get_all_gridpos(m.block)
    print(lt)
    # print(board[19][0])
