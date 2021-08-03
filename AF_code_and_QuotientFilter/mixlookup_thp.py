#图5实验
#使用GPU运行代码
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import sys
sys.path.append("C:/Users/fptjy/pybloom")

from pybloom import BloomFilter
import bitarray, math, time
from utils import range_fn
import random

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter

sys.path.append("C:/Users/fptjy/ArkFilter")
from Ark_Filter import Ark_Filter
import math
import numpy as np

from quotient_filter import QuotientFilter

mixlookup_thp_BF = []
mixlookup_thp_CF = []
mixlookup_thp_ArkF = []
mixlookup_thp_QF = []

#设置测试的次数
cishu = 30
for cs in range(cishu):

    # 测试插入随机字符串
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
    testdata = [0 for i in range(2**20)]
    for num in range(2**20):
        sa = []
        for i in range(16):
            sa.append(random.choice(alphabet))
        testdata[num] = "".join(sa)

    testdata1 = [0 for i in range(2**20)]
    for num in range(2**20):
        sa = []
        for i in range(17):
            sa.append(random.choice(alphabet))
        testdata1[num] = "".join(sa)

    #参数设置
    alpha = 0.95
    print("table occupancy:", alpha)

    rate_array = np.arange(0.025, 1, 0.05)
    for i in range(len(rate_array)):
        rate = rate_array[i]
        print("------------------------------------------")
        print("------------------------------------------")
        print("------------------------------------------")
        print("fraction of queries on existing items:", rate)

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

        f = BloomFilter(capacity=2 ** 20, error_rate=0.00001)
        for i in range_fn(int(alpha * len(testdata))):
            f.add(testdata[i], skip_check=True)

        cf = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19)
        for i in range(int(alpha * len(testdata))):
            cf.insert(testdata[i])

        ARK = Ark_Filter(capacity=2 ** 18)
        for i in range(int(alpha * len(testdata))):
            ARK.insert(testdata[i])

        qf = QuotientFilter()

        _testdata = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata[i] = testdata[i]

        _testdata1 = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata1[i] = testdata1[i]

        _testdata2 = [0 for i in range(int(alpha * qf.p))]
        for i in range(int(alpha * qf.p * rate)):
            _testdata2[i] = _testdata[i]
        for i in range(int(alpha * qf.p * rate), int(alpha * qf.p)):
            _testdata2[i] = _testdata1[i]
        state = np.random.get_state()
        np.random.shuffle(_testdata2)
        np.random.set_state(state)

        for i in range(int(alpha * qf.p)):
            qf.addKey(_testdata[i])

        # 随机查一定比例存在的对象

        start = time.time()
        for i in range(len(testdata2)):
            f.__contains__(testdata2[i])
        end = time.time()
        print("bloom filter:")
        print("{:5.3f} seconds to look up mixed item, {:10.2f} entries/second".format(
            end - start, len(testdata2) / (end - start)))
        mixlookup_thp_BF.append(len(testdata2) / (end - start))


        start = time.time()
        for i in range(len(testdata2)):
            cf.contains(testdata2[i])
        end = time.time()
        print("cuckoo filter:")
        print("{:5.3f} seconds to look up mixed item, {:10.2f} entries/second".format(
            end - start, len(testdata2) / (end - start)))
        mixlookup_thp_CF.append(len(testdata2) / (end - start))


        start = time.time()
        for i in range(len(testdata2)):
            ARK.contains(testdata2[i])
        end = time.time()
        print("ARK filter:")
        print("{:5.3f} seconds to look up mixed item, {:10.2f} entries/second".format(
            end - start, len(testdata2) / (end - start)))
        mixlookup_thp_ArkF.append(len(testdata2) / (end - start))


        start = time.time()
        for i in range(len(_testdata2)):
            qf.lookup(_testdata2[i])
        end = time.time()
        print("quotient filter:")
        print("{:5.3f} seconds to look up mixed item, {:10.2f} entries/second".format(
            end - start, len(_testdata2) / (end - start)))
        mixlookup_thp_QF.append(len(_testdata2) / (end - start))

mixlookup_thp_BF2 = [0 for i in range(20)]
mixlookup_thp_CF2 = [0 for i in range(20)]
mixlookup_thp_ArkF2 = [0 for i in range(20)]
mixlookup_thp_QF2 = [0 for i in range(20)]

for j in range(20):
    k = j
    for i in range(cishu):
        mixlookup_thp_BF2[j] += mixlookup_thp_BF[k]
        mixlookup_thp_CF2[j] += mixlookup_thp_CF[k]
        mixlookup_thp_ArkF2[j] += mixlookup_thp_ArkF[k]
        mixlookup_thp_QF2[j] += mixlookup_thp_QF[k]
        k += 20

for j in range(20):
    mixlookup_thp_BF2[j] = mixlookup_thp_BF2[j] / cishu
    mixlookup_thp_CF2[j] = mixlookup_thp_CF2[j] / cishu
    mixlookup_thp_ArkF2[j] = mixlookup_thp_ArkF2[j] / cishu
    mixlookup_thp_QF2[j] = mixlookup_thp_QF2[j] / cishu

print("#############混合查询的实验结果###########")
print("mixlookup_thp_BF")
print(mixlookup_thp_BF2)
print("mixlookup_thp_CF")
print(mixlookup_thp_CF2)
print("mixlookup_thp_ArkF")
print(mixlookup_thp_ArkF2)
print("mixlookup_thp_QF")
print(mixlookup_thp_QF2)




