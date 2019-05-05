# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/4/17
@IDE: PyCharm
"""
import gym_tetris
env = gym_tetris.make('Tetris-v0')

done = True
cnt = 0
for step in range(5000):
    if done:
        state = env.reset()
    env.render()
    state, reward, done, info = env.step(env.action_space.sample())
    cnt += reward
    if done:
        print("最终的奖励值为：{}".format(cnt))
        break
env.close()
