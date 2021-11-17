#####频数估计的查询实验（查询吞吐量，取正态分布，频数平均值取20）#####
import sys
import numpy as np
import math
import random
import time

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/ArkFilter_for_Counting")
from Counting_Ark_Filter import Counting_Ark_Filter

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/BF_contrast")

from Shifting_BF import Shifting_BloomFilter
from Adaptive_BF import Adaptive_BloomFilter

# 实验参数设置
cishu = 10

alpha = 0.95
size = 2 ** 18
capacity = size * 4

###准备数据集，生成服从均匀分布、正态分布和指数分布三种的三种数据集###

##分布的参数设置
normal_loc = 20
normal_scale = 4

###实验部分

##输出分布的参数配置
print("      ")
print("###分布参数的配置###")
print("正态分布的平均值为：", normal_loc)
print("正态分布的标准差为：", normal_scale)

print("  ")
print("###实验结果--混合查询吞吐量###")

##实现正态分布的随机抽样##
np.random.seed(1)
x1 = np.random.normal(loc=normal_loc, scale=normal_scale, size=capacity)

y1 = []
for i in range(len(x1)):
    z = math.ceil(x1[i])
    if z >= 1:
        y1.append(z)
    else:
        y1.append(1)

y = y1
##开始实验##

AF_result = []
ABF4_result = []
ABF8_result = []
SBF4_result = []
SBF8_result = []

rate_array = np.arange(0.025, 1, 0.05)
for i in range(len(rate_array)):
    rate = rate_array[i]
    print("fraction of queries on existing items:", rate)

    AF_result_temporary = []
    ABF4_result_temporary = []
    ABF8_result_temporary = []
    SBF4_result_temporary = []
    SBF8_result_temporary = []

    for times in range(cishu):

        # 测试插入随机字符串
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 测试查询的随机字符串（不存在的）
        testdata1 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(20):
                sa.append(random.choice(alphabet))
            testdata1[num2] = "".join(sa)

        # 根据rate设置随机查询存在对象的数据集合testdata2
        datasize = int(alpha * len(testdata))
        exist_num = int(rate * datasize)
        testdata2 = [0 for i in range(datasize)]
        for i in range(exist_num):
            testdata2[i] = testdata[i]
        for i in range(exist_num, datasize):
            testdata2[i] = testdata1[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        # ArkFilter的实验
        ARK = Counting_Ark_Filter(capacity=size)
        for i in range(int(alpha * len(testdata))):
            ARK.insert(testdata[i], y[i])
        # print("AF: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, ARK.size / (end - start)))

        start = time.time()
        for i in range(len(testdata2)):
            ARK.query(testdata2[i])
        end = time.time()
        AF_result_temporary.append(len(testdata2) / (end - start))

        # ABF使用4个哈希函数的实验
        ABF4 = Adaptive_BloomFilter(k=4,
                                    m=math.ceil(capacity * (20.014804508959585 + math.ceil(math.log(max(y), 2)))),
                                    max=max(y))
        for i in range(int(alpha * len(testdata))):
            ABF4.insert(testdata[i], y[i])
        # print("ABF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))

        start = time.time()
        for i in range(len(testdata2)):
            ABF4.query(testdata2[i])
        end = time.time()
        ABF4_result_temporary.append(len(testdata2) / (end - start))

        # ABF使用8个哈希函数的实验
        ABF8 = Adaptive_BloomFilter(k=8,
                                    m=math.ceil(capacity * (20.014804508959585 + math.ceil(math.log(max(y), 2)))),
                                    max=max(y))
        for i in range(int(alpha * len(testdata))):
            ABF8.insert(testdata[i], y[i])
        # print("ABF8: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))

        start = time.time()
        for i in range(len(testdata2)):
            ABF8.query(testdata2[i])
        end = time.time()
        ABF8_result_temporary.append(len(testdata2) / (end - start))

        # SBF使用4个哈希函数
        SBF4 = Shifting_BloomFilter(k=4,
                                    m=math.ceil(capacity * (20.014804508959585 + math.ceil(math.log(max(y), 2)))),
                                    max=max(y))
        for i in range(int(alpha * len(testdata))):
            SBF4.insert(testdata[i], y[i])
        # print("SBF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))

        start = time.time()
        for i in range(len(testdata2)):
            SBF4.query(testdata2[i])
        end = time.time()
        SBF4_result_temporary.append(len(testdata2) / (end - start))

        # SBF使用8个哈希函数
        SBF8 = Shifting_BloomFilter(k=8,
                                    m=math.ceil(capacity * (20.014804508959585 + math.ceil(math.log(max(y), 2)))),
                                    max=max(y))
        for i in range(int(alpha * len(testdata))):
            SBF8.insert(testdata[i], y[i])
        # print("SBF8: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))

        start = time.time()
        for i in range(len(testdata2)):
            SBF8.query(testdata2[i])
        end = time.time()
        SBF8_result_temporary.append(len(testdata2) / (end - start))

    AF_result.append(np.mean(AF_result_temporary))
    ABF4_result.append(np.mean(ABF4_result_temporary))
    ABF8_result.append(np.mean(ABF8_result_temporary))
    SBF4_result.append(np.mean(SBF4_result_temporary))
    SBF8_result.append(np.mean(SBF8_result_temporary))

print("混合查询吞吐量 of AF:", AF_result)
print("混合查询吞吐量 of ABF4:", ABF4_result)
print("混合查询吞吐量 of ABF8:", ABF8_result)
print("混合查询吞吐量 of SBF4:", SBF4_result)
print("混合查询吞吐量 of SBF8:", SBF8_result)

print("      ")
