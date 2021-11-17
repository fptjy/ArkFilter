#####topk在不同k下的实验#####
import sys
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from scipy import special  # doctest: +SKIP
from memory_profiler import profile

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/Space_saving_algorithm")
from SpaceSaving import SpaceSavingCounter

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/Lossy_Counting")
from LossyCounting import LossyCounting

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/HeavyKeeper")
from HeavyKeeper import HeavyKeeperSketch
from MinHeap import MinHeap

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/ArkFilter_for_Topk")
from Topk_Ark_Filter import Topk_Ark_Filter
# from AF_Topk_query
import AF_Topk_query as AF_Topk_que


def sampling_zipf(M, N, Skewness):
    result = []
    for i in range(M):
        p = 0
        for j in range(M):
            p += ((i + 1) / (j + 1)) ** Skewness
        result.append(int(N / p))
    return result


###测试字符串+6
number = 2 ** 14
mean = 2 ** 6
k = [200, 300, 400, 500, 600]
gama = 1.5
# print(number * mean)
print("实验参数")
print("k=", k)
print("Skewness =", gama)

result_precision_SS = []
result_precision_Lss = []
result_precision_HK = []
result_precision_AF = []

result_ARE_SS = []
result_ARE_Lss = []
result_ARE_HK = []
result_ARE_AF = []

for number_k in range(len(k)):

    temp_precision_SS = []
    temp_precision_Lss = []
    temp_precision_HK = []
    temp_precision_AF = []

    temp_ARE_SS = []
    temp_ARE_Lss = []
    temp_ARE_HK = []
    temp_ARE_AF = []

    for cishu in range(10):

        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(number)]
        for num in range(number):
            sa = []
            for i in range(45):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        topk_flow = testdata[:k[number_k]]

        frequency_rank = sampling_zipf(number, number * mean, gama)

        # print("frequency_rank[k[1]]", frequency_rank[k[number_k] - 1])
        # print(r)
        # print(np.sum(r))
        # print(r[500])

        data = []
        for i in range(number):
            for j in range(frequency_rank[i]):
                data.append(testdata[i])

        np.random.shuffle(data)

        """
        test of SpaceSaving
        """


        # @profile()
        def spcesaving_create():
            x = SpaceSavingCounter(1 / 546)
            return x


        # @profile()

        counter_SS = spcesaving_create()
        for i in range(len(data)):
            counter_SS.inc(data[i])
        result_Spacesaving_key = []
        result_Spacesaving_value = []

        for i in counter_SS.counts.keys():
            result_Spacesaving_key.append(i)
        for i in counter_SS.counts.values():
            result_Spacesaving_value.append(i)

        true_number_ss = 0
        for i in range(len(result_Spacesaving_key)):
            if result_Spacesaving_key[i] in topk_flow:
                true_number_ss += 1
        precision_SS = true_number_ss / k[number_k]

        estimate_error_ss = 0
        for i in range(len(result_Spacesaving_value)):
            if result_Spacesaving_key[i] in topk_flow:
                index = topk_flow.index(result_Spacesaving_key[i])
                estimate_error_ss += abs(frequency_rank[index] - result_Spacesaving_value[i]) / frequency_rank[index]
        ARE_SS = estimate_error_ss / true_number_ss

        # print("space consume", sys.getsizeof(counter_SS))
        # print(precision_SS)
        # print(ARE_SS)

        temp_ARE_SS.append(ARE_SS)
        temp_precision_SS.append(precision_SS)

        """
        test of LossyCounting
        """


        # print("frequency_rank[k[1]] / number * mean", frequency_rank[k[1] - 1] / (number * mean))

        # @profile()
        def create_Lss():
            x = LossyCounting(0.00065)
            return x


        counter_Lss = create_Lss()

        jilu = []
        for i in range(len(data)):
            counter_Lss.addCount(data[i])
            jilu.append(counter_Lss.add_new_number - counter_Lss.del_number)

        true_number_Lss = 0
        estimate_error_Lss = 0
        for item, count in sorted(counter_Lss.iterateOverThresholdCount(frequency_rank[k[number_k]]),
                                  key=lambda x: x[1]):
            if item in topk_flow:
                true_number_Lss += 1
                index = topk_flow.index(item)
                estimate_error_Lss += abs(frequency_rank[index] - count) / frequency_rank[index]

        precision_Lss = true_number_Lss / k[number_k]
        ARE_Lss = estimate_error_Lss / true_number_Lss

        # print("space consume", sys.getsizeof(counter_Lss))
        # print(precision_Lss)
        # print(ARE_Lss)
        #
        # print("LSS_max_size:", np.max(jilu))

        temp_ARE_Lss.append(ARE_Lss)
        temp_precision_Lss.append(precision_Lss)

        """
        test of HeavyKeeper
        """


        # @profile()
        def create_HeavyKeeper():
            x = HeavyKeeperSketch(width=int(2 ** 12), depth=4, seeds=[0, 1, 2, 3], finger_size=2 ** 12, base=1.08)
            return x


        minheap = MinHeap(maxsize=k[number_k])
        HKS = create_HeavyKeeper()
        for i in range(len(data)):
            HKS.insert(data[i])
        for i in range(len(testdata)):
            lookup = HKS.query(testdata[i])
            minheap.heavy_keep(testdata[i], lookup)

        true_number_HK = 0
        estimate_error_HK = 0
        for i in range(minheap.maxsize):
            if minheap._elements[i][0] in topk_flow:
                true_number_HK += 1
                index = topk_flow.index(minheap._elements[i][0])
                estimate_error_HK += abs(frequency_rank[index] - minheap._elements[i][1]) / frequency_rank[index]

        precision_HK = true_number_HK / k[number_k]
        ARE_HK = estimate_error_HK / true_number_HK

        # print("space consume", sys.getsizeof(HKS))
        # print(precision_HK)
        # print(ARE_HK)

        temp_ARE_HK.append(ARE_HK)
        temp_precision_HK.append(precision_HK)

        """
        test of AFFilter_topk
        """


        # @profile()
        def create_TopK_AF():
            x = Topk_Ark_Filter(capacity=2 ** 12, bucket_size=4)
            return x


        AF = create_TopK_AF()
        for i in range(len(data)):
            AF.insert(data[i])

        topk_flow_finger = []
        for item in topk_flow:
            topk_flow_finger.append(AF._get_fingerprint(item))

        result_AF = AF_Topk_que.maxheap_for_topk(AF, number_of_floors=1, k=k[number_k])

        result_AF_finger = []
        result_AF_count = []
        for i in result_AF:
            result_AF_finger.append(i[0])
            result_AF_count.append(i[1])

        true_number_AF = 0
        estimate_error_AF = 0

        for i in range(len(result_AF_finger)):
            if result_AF_finger[i] in topk_flow_finger:
                true_number_AF += 1
                index = topk_flow_finger.index(result_AF_finger[i])
                estimate_error_AF += abs(frequency_rank[index] - result_AF_count[i]) / frequency_rank[index]

        precision_AF = true_number_AF / k[number_k]
        ARE_AF = estimate_error_AF / true_number_AF

        # print("space consume", sys.getsizeof(AF))
        # print(precision_AF)
        # print(ARE_AF)

        temp_ARE_AF.append(ARE_AF)
        temp_precision_AF.append(precision_AF)


        # def create_TopK_AF():
        #     x = Topk_Ark_Filter(capacity=2 ** 12, bucket_size=4)
        #     return x
        #
        #
        # AF = create_TopK_AF()
        # for i in range(len(data)):
        #     AF.insert(data[i])
        #
        # topk_flow_finger = []
        # for item in topk_flow:
        #     topk_flow_finger.append(AF._get_fingerprint(item))
        #
        # result_AF = AF_Topk_que.minheap_for_topk(AF, number_of_floors=2, k=k[number_k])
        #
        # true_number_AF = 0
        # estimate_error_AF = 0
        #
        # for i in range(result_AF.maxsize):
        #     if result_AF._elements[i][0] in topk_flow_finger:
        #         true_number_AF += 1
        #         index = topk_flow_finger.index(result_AF._elements[i][0])
        #         estimate_error_AF += abs(frequency_rank[index] - result_AF._elements[i][1]) / frequency_rank[index]
        #
        # precision_AF = true_number_AF / k[number_k]
        # ARE_AF = estimate_error_AF / true_number_AF
        #
        # # print("space consume", sys.getsizeof(AF))
        # # print(precision_AF)
        # # print(ARE_AF)
        #
        # temp_ARE_AF.append(ARE_AF)
        # temp_precision_AF.append(precision_AF)

    result_precision_SS.append(np.mean(temp_precision_SS))
    result_precision_Lss.append(np.mean(temp_precision_Lss))
    result_precision_HK.append(np.mean(temp_precision_HK))
    result_precision_AF.append(np.mean(temp_precision_AF))

    result_ARE_SS.append(np.mean(temp_ARE_SS))
    result_ARE_Lss.append(np.mean(temp_ARE_Lss))
    result_ARE_HK.append(np.mean(temp_ARE_HK))
    result_ARE_AF.append(np.mean(temp_ARE_AF))

print("自变量为k的实验结果")
print("Precision of SpaceSaving:", result_precision_SS)
print("Precision of LossyCounting:", result_precision_Lss)
print("Precision of HeavyKeeper:", result_precision_HK)
print("Precision of ArkFilter:", result_precision_AF)

print(" ")
print("ARE of SpaceSaving:", result_ARE_SS)
print("ARE of LossyCounting:", result_ARE_Lss)
print("ARE of HeavyKeeper:", result_ARE_HK)
print("ARE of ArkFilter:", result_ARE_AF)
