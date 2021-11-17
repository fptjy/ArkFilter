# 图7实验
import sys

sys.path.append("C:/Users/fptjy/pybloom")

from pybloom import BloomFilter
import bitarray, math, time
from utils import range_fn
import random

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter

sys.path.append("C:/Users/fptjy/ArkFilter_experiment/ArkFilter")
from Ark_Filter import Ark_Filter
import math
import numpy as np
import datetime
from quotient_filter import QuotientFilter

insert_thp_BF = []
insert_thp_CF = []
insert_thp_ArkF = []
insert_thp_QF = []

cishu = 80
print("测试次数为：", cishu)
delta = 5000
print("general delta:", delta)
qf_delta = 5000
print("delta for QF:", qf_delta)
print("需要补上空间利用率为0.975时的实验结果")

for cs in range(cishu):

    # 测试插入随机字符串
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
    testdata = [0 for i in range(2 ** 20)]
    for num in range(2 ** 20):
        sa = []
        for i in range(16):
            sa.append(random.choice(alphabet))
        testdata[num] = "".join(sa)

    # 参数设置并测试
    # alpha_array = [0.025, 0.075, 0.125, 0.175]
    alpha_array = np.arange(0.025, 0.95, 0.05)
    for i in range(len(alpha_array)):

        # print("##########################################")
        # print("##########################################")
        # print("##########################################")

        alpha = alpha_array[i]
        # print("table occupancy:", alpha)

        # 先存储达到alpha时的一定数量的对象
        f = BloomFilter(capacity=2 ** 20, error_rate=0.000015)
        for i in range_fn(int(alpha * len(testdata) - delta / 2)):
            f.add(testdata[i], skip_check=True)

        cf = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            cf.insert(testdata[i])

        ARK = Ark_Filter(capacity=2 ** 18)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            ARK.insert(testdata[i])

        qf = QuotientFilter()
        _testdata = [0 for i in range(qf.p * 2)]
        for i in range(qf.p * 2):
            _testdata[i] = testdata[i]
        for i in range(int(alpha * qf.p - delta / 2)):
            qf.addKey(_testdata[i])

        # # 开始测试达到alpha时，插入delta个对象的吞吐量
        start = datetime.datetime.now()
        for i in range(delta):
            f.add(testdata[int(alpha * len(testdata) - delta / 2) + i], skip_check=True)
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s * 10 ** 6 + time_ms
        # print("用的微妙", time_ms)
        # print("时间消耗：", time_consume)
        if time_consume == 0:
            insert_thp_BF.append(0)
        else:
            insert_thp_BF.append(delta * 10 ** 6 / time_consume)
        # print("bloom filter:")
        # print("{:5.3f} microseconds to insert delta items, {:10.2f} entries/microsecond".format(
        #     time_consume, delta / time_consume))
        #
        # insert_thp_BF.append(delta * 10 ** 6 / time_consume)

        start = datetime.datetime.now()
        for i in range(delta):
            cf.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s * 10 ** 6 + time_ms
        # print("用的微妙", time_ms)
        # print("时间消耗：", time_consume)
        if time_consume == 0:
            insert_thp_CF.append(0)
        else:
            insert_thp_CF.append(delta * 10 ** 6 / time_consume)

        # print("cuckoo filter:")
        # print("{:5.3f} microseconds to insert delta items, {:10.2f} entries/microsecond".format(
        #     time_consume, delta / time_consume))
        # insert_thp_CF.append(delta * 10 ** 6 / time_consume)

        start = datetime.datetime.now()
        for i in range(delta):
            ARK.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s * 10 ** 6 + time_ms
        # print("用的微妙", time_ms)
        # print("时间消耗：", time_consume)
        if time_consume == 0:
            insert_thp_ArkF.append(0)
        else:
            insert_thp_ArkF.append(delta * 10 ** 6 / time_consume)
        # print("Ark filter:")
        # print("{:5.3f} microseconds to insert delta items, {:10.2f} entries/microsecond".format(
        #     time_consume, delta / time_consume))
        # insert_thp_ArkF.append(delta * 10 ** 6 / time_consume)

        start = datetime.datetime.now()
        for i in range(qf_delta):
            qf.addKey(_testdata[int(alpha * len(_testdata) - qf_delta / 2) + i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s * 10 ** 6 + time_ms
        # print("用的微妙", time_ms)
        # print("时间消耗：", time_consume)
        if time_consume == 0:
            insert_thp_QF.append(0)
        else:
            insert_thp_QF.append(qf_delta * 10 ** 6 / time_consume)

        # print("Quotient filter:")
        # print("qf_delta=", qf_delta)
        # print("{:5.3f} microseconds to insert delta items, {:10.2f} entries/microsecond".format(
        #     time_consume, qf_delta / time_consume))
        # insert_thp_QF.append(qf_delta * 10 ** 6 / time_consume)

    # # 参数设置并测试
    # alpha_array = np.arange(0.025, 1, 0.05)
    # for i in range(len(alpha_array)):
    #     # print("##########################################")
    #     # print("##########################################")
    #     # print("##########################################")
    #
    #     alpha = alpha_array[i]
    #     # print("table occupancy:", alpha)
    #     # delta = 5000
    #     # print("delta items:", delta)
    #
    #
    #     # 先存储达到alpha时的一定数量的对象
    #     f = BloomFilter(capacity=2 ** 20, error_rate=0.00001)
    #     for i in range_fn(int(alpha * len(testdata) - delta / 2)):
    #         f.add(testdata[i], skip_check=True)
    #
    #     cf = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19)
    #     for i in range(int(alpha * len(testdata) - delta / 2)):
    #         cf.insert(testdata[i])
    #
    #     ARK = Ark_Filter(capacity=2 ** 18)
    #     for i in range(int(alpha * len(testdata) - delta / 2)):
    #         ARK.insert(testdata[i])
    #
    #     qf = QuotientFilter()
    #     _testdata = [0 for i in range(qf.p)]
    #     for i in range(qf.p):
    #         _testdata[i] = testdata[i]
    #     for i in range(int(alpha * qf.p - qf_delta / 2)):
    #         qf.addKey(_testdata[i])
    #
    #     # 开始测试达到alpha时，插入delta个对象的吞吐量
    #     start = time.time()
    #     for i in range(delta):
    #         f.add(testdata[int(alpha * len(testdata) - delta / 2) + i], skip_check=True)
    #     end = time.time()
    #     # print("bloom filter:")
    #     # print("{:5.3f} seconds to insert delta items, {:10.2f} entries/second".format(
    #     #     end - start, delta / (end - start)))
    #     insert_thp_BF.append(delta / (end - start))
    #
    #     start = time.time()
    #     for i in range(delta):
    #         cf.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
    #     end = time.time()
    #     # print("cuckoo filter:")
    #     # print("{:5.3f} seconds to insert delta items, {:10.2f} entries/second".format(
    #     #     end - start, delta / (end - start)))
    #     insert_thp_CF.append(delta / (end - start))
    #
    #     start = time.time()
    #     for i in range(delta):
    #         ARK.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
    #     end = time.time()
    #     # print("Ark filter:")
    #     # print("{:5.3f} seconds to insert delta items, {:10.2f} entries/second".format(
    #     #     end - start, delta / (end - start)))
    #     insert_thp_ArkF.append(delta / (end - start))
    #
    #     start = time.time()
    #     for i in range(qf_delta):
    #         qf.addKey(_testdata[int(alpha * len(_testdata) - qf_delta / 2) + i])
    #     end = time.time()
    #     # print("Quotient filter:")
    #     # print("{:5.3f} seconds to insert delta items, {:10.2f} entries/second".format(
    #     #     end - start, delta / (end - start)))
    #     insert_thp_QF.append(qf_delta / (end - start))
#
# insert_thp_BF2 = [0 for i in range(20)]
# insert_thp_CF2 = [0 for i in range(20)]
# insert_thp_ArkF2 = [0 for i in range(20)]
# insert_thp_QF2 = [0 for i in range(20)]
#
# for j in range(20):
#     k = j
#     for i in range(cishu):
#         insert_thp_BF2[j] += insert_thp_BF[k]
#         insert_thp_CF2[j] += insert_thp_CF[k]
#         insert_thp_ArkF2[j] += insert_thp_ArkF[k]
#         insert_thp_QF2[j] += insert_thp_QF[k]
#         k += 20
#
# count_BF = [0 for i in range(20)]
# count_CF = [0 for i in range(20)]
# count_ArkF = [0 for i in range(20)]
# count_QF = [0 for i in range(20)]
#
# for j in range(20):
#     k = j
#     for i in range(cishu):
#         if insert_thp_BF[k] == 0:
#             count_BF[j] += 1
#         if insert_thp_CF[k] == 0:
#             count_CF[j] += 1
#         if insert_thp_ArkF[k] == 0:
#             count_ArkF[j] += 1
#         if insert_thp_QF[k] == 0:
#             count_QF[j] += 1
#         k += 20
#
# print("count_BF为：", count_BF)
# print("count_CF为：", count_CF)
# print("count_ArkF为：", count_ArkF)
# print("count_QF为：", count_QF)
#
# for j in range(20):
#     insert_thp_BF2[j] = insert_thp_BF2[j] / (cishu - count_BF[j])
#     insert_thp_CF2[j] = insert_thp_CF2[j] / (cishu - count_CF[j])
#     insert_thp_ArkF2[j] = insert_thp_ArkF2[j] / (cishu - count_ArkF[j])
#     insert_thp_QF2[j] = insert_thp_QF2[j] / (cishu - count_QF[j])
#
# print("##############实验结果###############")
# print("insert_thp_BF", insert_thp_BF2)
# print("insert_thp_CF", insert_thp_CF2)
# print("insert_thp_ArkF", insert_thp_ArkF2)
# print("insert_thp_QF", insert_thp_QF2)

length = len(alpha_array)

insert_thp_BF2 = [0 for i in range(length)]
insert_thp_CF2 = [0 for i in range(length)]
insert_thp_ArkF2 = [0 for i in range(length)]
insert_thp_QF2 = [0 for i in range(length)]

for j in range(length):
    k = j
    for i in range(cishu):
        insert_thp_BF2[j] += insert_thp_BF[k]
        insert_thp_CF2[j] += insert_thp_CF[k]
        insert_thp_ArkF2[j] += insert_thp_ArkF[k]
        insert_thp_QF2[j] += insert_thp_QF[k]
        k += length

count_BF = [0 for i in range(length)]
count_CF = [0 for i in range(length)]
count_ArkF = [0 for i in range(length)]
count_QF = [0 for i in range(length)]

for j in range(length):
    k = j
    for i in range(cishu):
        if insert_thp_BF[k] == 0:
            count_BF[j] += 1
        if insert_thp_CF[k] == 0:
            count_CF[j] += 1
        if insert_thp_ArkF[k] == 0:
            count_ArkF[j] += 1
        if insert_thp_QF[k] == 0:
            count_QF[j] += 1
        k += length

print("count_BF为：", count_BF)
print("count_CF为：", count_CF)
print("count_ArkF为：", count_ArkF)
print("count_QF为：", count_QF)

for j in range(length):
    insert_thp_BF2[j] = insert_thp_BF2[j] / (cishu - count_BF[j])
    insert_thp_CF2[j] = insert_thp_CF2[j] / (cishu - count_CF[j])
    insert_thp_ArkF2[j] = insert_thp_ArkF2[j] / (cishu - count_ArkF[j])
    insert_thp_QF2[j] = insert_thp_QF2[j] / (cishu - count_QF[j])

print("##############实验结果###############")
print("insert_thp_BF", insert_thp_BF2)
print("insert_thp_CF", insert_thp_CF2)
print("insert_thp_ArkF", insert_thp_ArkF2)
print("insert_thp_QF", insert_thp_QF2)