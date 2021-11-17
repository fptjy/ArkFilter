import random
import numpy as np
import sys
import csv
import time

import Compact_Filetr as Compact_Filetr
import subtract_intersection_Filter as  subtract_intersection

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/ArkFilter")
from Ark_Filter import Ark_Filter

capacity = 2 ** 20
rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cishu = 10

print("rate:", rate)

compact_result = []
for canshu in range(len(rate)):
    alpha_B = rate[canshu]
    result = []
    for cs in range(cishu):
        # 数据集1
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 数据集2
        testdata1 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata1[num2] = "".join(sa)

        # 创造Filter_A和Filter_B
        AF_A = Ark_Filter(capacity=2 ** 18)
        AF_B = Ark_Filter(capacity=2 ** 18)

        alpha_A = 0.05
        for i in range(int(alpha_A * len(testdata))):
            AF_A.insert(testdata[i])

        for i in range(int(alpha_B * len(testdata1))):
            AF_B.insert(testdata1[i])

        start = time.time()
        Compact_Filetr.compact_ArkFilter(AF_A, AF_B)
        end = time.time()
        time_consume = end - start
        result.append(time_consume)
    compact_result.append(np.mean(result))

print("compact_result", compact_result)

intersection_result = []
alpha = 0.95
for canshu in range(len(rate)):
    rate_exist = rate[canshu]
    result2 = []
    for cs in range(cishu):
        # 数据集1
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 数据集2
        testdata1 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata1[num2] = "".join(sa)

        # 数据集1和2按一定比例混合而成的数据集
        datasize = capacity
        exist_num = int(rate_exist * datasize)
        testdata2 = [0 for i in range(datasize)]
        for i in range(exist_num):
            testdata2[i] = testdata[i]
        for i in range(exist_num, datasize):
            testdata2[i] = testdata1[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        # 创造Filter_A和Filter_B
        AF_A = Ark_Filter(capacity=2 ** 18)
        AF_B = Ark_Filter(capacity=2 ** 18)

        for i in range(int(alpha * len(testdata))):
            AF_A.insert(testdata[i])

        for i in range(int(alpha * len(testdata2))):
            AF_B.insert(testdata2[i])

        start = time.time()
        subtract_intersection.intersection_ArkFilter(AF_A, AF_B)
        end = time.time()
        time_consume = end - start
        result2.append(time_consume)
    intersection_result.append(np.mean(result2))

print("intersection_result", intersection_result)


subtract_result = []
alpha = 0.95
for canshu in range(len(rate)):
    rate_exist = rate[canshu]
    result3 = []
    for cs in range(cishu):
        # 数据集1
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 数据集2
        testdata1 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata1[num2] = "".join(sa)

        # 数据集1和2按一定比例混合而成的数据集
        datasize = capacity
        exist_num = int(rate_exist * datasize)
        testdata2 = [0 for i in range(datasize)]
        for i in range(exist_num):
            testdata2[i] = testdata[i]
        for i in range(exist_num, datasize):
            testdata2[i] = testdata1[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        # 创造Filter_A和Filter_B
        AF_A = Ark_Filter(capacity=2 ** 18)
        AF_B = Ark_Filter(capacity=2 ** 18)

        for i in range(int(alpha * len(testdata))):
            AF_A.insert(testdata[i])

        for i in range(int(alpha * len(testdata2))):
            AF_B.insert(testdata2[i])

        start = time.time()
        subtract_intersection.subtract_ArkFilter(AF_A, AF_B)
        end = time.time()
        time_consume = end - start
        result3.append(time_consume)
    subtract_result.append(np.mean(result3))

print("subtract_result", subtract_result)