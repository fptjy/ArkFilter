#####频数估计的存储实验#####
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

#实验参数设置
cishu = 10

alpha = 0.95
size = 2**18
capacity = size*4

###准备数据集，生成服从均匀分布、正态分布和指数分布三种的三种数据集###

##实现正态分布的随机抽样##
np.random.seed(1)
x1 = np.random.normal(loc=30, scale=10, size=capacity)

y1 = []
for i in range(len(x1)):
    z = math.ceil(x1[i])
    if z >= 1:
        y1.append(z)
    else:
        y1.append(1)

##均匀分布##
# numpy.random.rand产生均匀分布的随机数
np.random.seed(2)
x2 = np.random.uniform(15, 45, size=capacity)
y2 = []
for i in range(len(x2)):
    z = math.ceil(x2[i])
    if z >= 1:
        y2.append(z)
    else:
        y2.append(1)

##指数分布##
np.random.seed(3)
x3 = np.random.exponential(30, size=capacity)
y3 = []
for i in range(len(x3)):
    z = math.ceil(x3[i])
    if z >= 1:
        y3.append(z)
    else:
        y3.append(1)

data = [y1, y2, y3]

##开始实验##
Kinds_of_data = ["正态分布", "均匀分布", "指数分布"]
for kinds in range(len(Kinds_of_data)):
    print(Kinds_of_data[kinds])
    y = data[kinds]

    AF_result = []
    ABF4_result = []
    ABF8_result = []
    SBF4_result = []
    SBF8_result = []

    for times in range(cishu):

        # 测试插入随机字符串
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        #ArkFilter的实验
        ARK = Counting_Ark_Filter(capacity=size)
        start = time.time()
        for i in range(int(alpha*len(testdata))):
            ARK.insert(testdata[i], y[i])
        end = time.time()
        # print("AF: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, ARK.size / (end - start)))
        AF_result.append(int(alpha*len(testdata)) / (end - start))

        #ABF使用4个哈希函数的实验
        ABF4 = Adaptive_BloomFilter(k=4, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
        start = time.time()
        for i in range(int(alpha*len(testdata))):
            ABF4.insert(testdata[i], y[i])
        end = time.time()
        # print("ABF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        ABF4_result.append(int(alpha*len(testdata)) / (end - start))

        #ABF使用8个哈希函数的实验
        ABF8 = Adaptive_BloomFilter(k=8, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
        start = time.time()
        for i in range(int(alpha*len(testdata))):
            ABF8.insert(testdata[i], y[i])
        end = time.time()
        # print("ABF8: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        ABF8_result.append(int(alpha*len(testdata)) / (end - start))

        #SBF使用4个哈希函数
        SBF4 = Shifting_BloomFilter(k=4, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
        start = time.time()
        for i in range(int(alpha*len(testdata))):
            SBF4.insert(testdata[i], y[i])
        end = time.time()
        # print("SBF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        SBF4_result.append(int(alpha*len(testdata)) / (end - start))

        #SBF使用8个哈希函数
        SBF8 = Shifting_BloomFilter(k=8, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
        start = time.time()
        for i in range(int(alpha*len(testdata))):
            SBF8.insert(testdata[i], y[i])
        end = time.time()
        # print("SBF8: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        SBF8_result.append(int(alpha*len(testdata)) / (end - start))

    print("Insertion thp of AF:", np.mean(AF_result))
    print("Insertion thp of ABF4:", np.mean(ABF4_result))
    print("Insertion thp of ABF8:", np.mean(ABF8_result))
    print("Insertion thp of SBF4:", np.mean(SBF4_result))
    print("Insertion thp of SBF8:", np.mean(SBF8_result))
    print("      ")
