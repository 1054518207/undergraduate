# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/4/23
@IDE: PyCharm
"""
import games
import numpy as np
import sys
import multiprocessing as mp

def init():
    env = games.make("Tetris-v0")

    done = True
    cnt = 0
    # np.set_printoptions(threshold=sys.maxsize)
    for step in range(5000):
        if done:
            state = env.reset()
        # env.render("rgb_array")
        env.render()
        state, reward, done, info = env.step(env.action_space.sample())
        cnt += reward
        # print(state)
        if done:
            print(type(state))
            print("最终的奖励值为：{}".format(cnt))
            break

    env.close()

if __name__ == '__main__':
    p1 = mp.Process(target=init, name="p1")
    p1.start()
    init()
    p1.join()
