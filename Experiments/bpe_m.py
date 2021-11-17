# #ArkFilter其假阳率、单位对象比特数与filter的大小关系
# import sys
# sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/ArkFilter")
# from ArkFilter import Ark_Filter
# import math
# import numpy as np
# import random
# import datetime
#
# average_bit = []
# fp_result = []
#
# """Test performance of ArkFilter at a set capacity and error rate."""
#
# capacity_array = [2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11, 2 ** 12, 2 ** 13, 2 ** 14, 2 ** 15, 2 ** 16, 2 ** 17, 2 ** 18, 2 ** 19, 2 ** 20, 2 ** 21]
# # capacity_array = [2 ** 18]
# alpha = 0.95
# print("table occupancy alpha:", alpha)
#
#
# cishu = 10
# for cs in range(cishu):
#
#     # 测试插入随机字符串
#     alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
#     testdata = [0 for i in range(2 ** 23)]
#     for num in range(2 ** 23):
#         sa = []
#         for i in range(16):
#             sa.append(random.choice(alphabet))
#         testdata[num] = "".join(sa)
#
#     testdata1 = [0 for i in range(2 ** 23)]
#     for num in range(2 ** 23):
#         sa = []
#         for i in range(17):
#             sa.append(random.choice(alphabet))
#         testdata1[num] = "".join(sa)
#
#     for j in range(len(capacity_array)):
#         filter_size = capacity_array[j]
#
#         ARK = Ark_Filter(capacity=filter_size)
#
#         print("##########################################")
#         print("size of Ark_filter:", ARK.capacity * ARK.bucket_size)
#         for i in range(int(alpha * ARK.capacity * ARK.bucket_size)):
#             ARK.insert(testdata[i])
#         print("ARK.size:", ARK.size)
#         print("对象的平均bit数：", (ARK.capacity * ARK.bucket_size / ARK.size * math.log2(ARK.capacity)) / 2 + 1)
#         average_bit.append((ARK.capacity * ARK.bucket_size / ARK.size * math.log2(ARK.capacity)) / 2 + 1)
#
#         fp = 0
#         for i in range(int(alpha * ARK.capacity * ARK.bucket_size)):
#             if ARK.contains(testdata1[i]):
#                 fp += 1
#         print("fp rate:", fp / int(alpha * ARK.capacity * ARK.bucket_size))
#         fp_result.append(fp / int(alpha * ARK.capacity * ARK.bucket_size))
#
# average_bit2 = [0 for i in range(len(capacity_array))]
# fp_result2 = [0 for i in range(len(capacity_array))]
#
# for j in range(len(capacity_array)):
#     k = j
#     for i in range(cishu):
#         average_bit2[j] += average_bit[k]
#         fp_result2[j] += fp_result[k]
#         k += len(capacity_array)
#
# for i in range(len(capacity_array)):
#     average_bit2[i] = average_bit2[i] / cishu
#     fp_result2[i] = fp_result2[i] / cishu
#
#
# print("##############实验结果###################")
# print("对象的平均比特数实验结果：", average_bit2)
# print("假阳率的实验结果：", fp_result2)


#####仅测试空间利用率#####
#ArkFilter其假阳率、单位对象比特数与filter的大小关系
import sys
sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/ArkFilter")
from Ark_Filter import Ark_Filter
import math
import numpy as np
import random
import datetime


occupancy = []

"""Test performance of ArkFilter at a set capacity and error rate."""

capacity_array = [2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11, 2 ** 12, 2 ** 13, 2 ** 14, 2 ** 15, 2 ** 16, 2 ** 17, 2 ** 18, 2 ** 19, 2 ** 20, 2 ** 21]
# capacity_array = [2 ** 18]
alpha = 0.95
print("table occupancy alpha:", alpha)


cishu = 1
for cs in range(cishu):

    # 测试插入随机字符串
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
    testdata = [0 for i in range(2 ** 23)]
    for num in range(2 ** 23):
        sa = []
        for i in range(16):
            sa.append(random.choice(alphabet))
        testdata[num] = "".join(sa)


    for j in range(len(capacity_array)):
        filter_size = capacity_array[j]

        ARK = Ark_Filter(capacity=filter_size)

        print("##########################################")
        print("size of Ark_filter:", ARK.capacity * ARK.bucket_size)
        for i in range(int(alpha * ARK.capacity * ARK.bucket_size)):
            ARK.insert(testdata[i])
        result = ARK.size / (ARK.capacity * ARK.bucket_size)
        print("Occupancy of ARK:", result)
        occupancy.append(result)


occupancy2 = [0 for i in range(len(capacity_array))]

for j in range(len(capacity_array)):
    k = j
    for i in range(cishu):
        occupancy2[j] += occupancy[k]
        k += len(capacity_array)

for i in range(len(capacity_array)):
    occupancy2[i] = occupancy2[i] / cishu


print("##############实验结果###################")
print("AF不同m下空间占用率的实验结果：", occupancy2)

