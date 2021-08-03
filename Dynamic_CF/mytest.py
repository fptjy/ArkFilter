import random
from cuckoofilter import CuckooFilter
import time
import Dynamic_cuckoo_filter
from cuckoofilter_murmurhash import CuckooFilter_mur

"""
#Read insertion data and data preprocess
"""
raw_data1 = []
with open('C:/Users/fptjy/ArkFilter_experiment/experiment/IP_final_min_int_sort.csv', 'r') as fin:
    for line in fin:
        raw_data1.append(line.replace("\n", ""))
fin.close()

# raw_data1 = []
# delta = 100000
# for i in range(len(raw_data0) - delta):
#     raw_data1.append(raw_data0[i])

insert_result = [[]]
tem = 0
for i in range(len(raw_data1)):

    x = int(raw_data1[i].split(",")[1])
    y = raw_data1[i].split(",")[0]
    if x == tem:
        insert_result[x].append(y)
    elif x == tem + 1:
        insert_result.append([])
        insert_result[x].append(y)
        tem += 1
    else:
        distance = x - tem
        for j in range(distance - 1):
            insert_result.append(["non"])
            tem += 1
        insert_result.append([])
        insert_result[x].append(y)
        tem += 1

print(len(insert_result))  # 81230

"""
#Read deletion data and data preprocess
"""
raw_data2 = []
with open('C:/Users/fptjy/ArkFilter_experiment/experiment/IP_final_max_int_sort.csv', 'r') as fin:
    for line in fin:
        raw_data2.append(line.replace("\n", ""))
fin.close()

delete_result = [[]]
tem = 0
for i in range(len(raw_data2)):

    x = int(raw_data2[i].split(",")[1])
    y = raw_data2[i].split(",")[0]
    if x == tem:
        delete_result[x].append(y)
    elif x == tem + 1:
        delete_result.append([])
        delete_result[x].append(y)
        tem += 1
    else:
        distance = x - tem
        for j in range(distance - 1):
            delete_result.append(["non"])
            tem += 1
        delete_result.append([])
        delete_result[x].append(y)
        tem += 1

##过滤掉到达但未离开的元素
CF_filtrate = CuckooFilter(capacity=2 ** 21, bucket_size=4, fingerprint_size=20)
# CF_mur_filter = CuckooFilter_mur(capacity=2 ** 21, bucket_size=4, fingerprint_size=18)
for i in range(len(delete_result)):
    if delete_result[i] == "non":
        print("non appear in delete")
    else:
        for j in range(len(delete_result[i])):
            CF_filtrate.insert(delete_result[i][j])
            # CF_mur_filter.insert(delete_result[i][j])

count = 0
for i in range(len(insert_result)):
    if insert_result[i] == "non":
        print("non appear in insert")
    else:
        for j in range(len(insert_result[i])):
            # if not CF_filtrate.contains(insert_result[i][j]) or not CF_mur_filter.contains(insert_result[i][j]):
            if not CF_filtrate.contains(insert_result[i][j]):
                count += 1
                insert_result[i][j] = "extra_element"
print(count)

count2 = 0
for i in range(len(insert_result)):
    while "extra_element" in insert_result[i]:
        insert_result[i].remove("extra_element")
        count2 += 1
print(count2)

# ##开始存储
# CFCF = CuckooFilter(capacity=2 ** 21, bucket_size=4, fingerprint_size=13)
#
# from Dynamic_cuckoo_filter import single_CF
# import Dynamic_cuckoo_filter as CF_d_o
#
# DCF_4 = single_CF(item_num=2 ** 15, fp=0.00048, exp_block_num=4)
#
# DCF_4_test_result = []
# CFCF_test_result = []
#
# for i in range(len(insert_result)):
#     if insert_result[i] == "non" or len(insert_result[i]) == 0:
#         print("non appear in insert_result", i)
#
#         CF_d_o.dcf_delete(data=delete_result[i], sketch=DCF_4)
#         CF_d_o.dcf_compact(sketch=DCF_4)
#
#         for l in range(len(delete_result[i])):
#             CFCF.delete(delete_result[i][l])
#
#         CFCF_test_result.append(CFCF.size)
#
#         x2 = len(DCF_4) * DCF_4[0].capacity * 4
#         DCF_4_test_result.append(x2)
#
#
#     else:
#         # DCF_4
#         CF_d_o.dcf_insert(data=insert_result[i], sketch=DCF_4)
#         # for j in range(len(delete_result[i])):
#         #     CF_d_o.dcf_delete(data=delete_result[i][j], sketch=DCF_4)
#         CF_d_o.dcf_delete(data=delete_result[i], sketch=DCF_4)
#         CF_d_o.dcf_compact(sketch=DCF_4)
#
#         for j in range(len(insert_result[i])):
#             CFCF.insert(insert_result[i][j])
#         for l in range(len(delete_result[i])):
#             CFCF.delete(delete_result[i][l])
#
#         CFCF_test_result.append(CFCF.size)
#
#         x2 = len(DCF_4) * DCF_4[0].capacity * 4
#         DCF_4_test_result.append(x2)
#
# for i in range(len(delete_result) - len(insert_result)):
#
#     # DCF_4
#     CF_d_o.dcf_delete(data=delete_result[i + len(insert_result)], sketch=DCF_4)
#     CF_d_o.dcf_compact(sketch=DCF_4)
#
#     for l in range(len(delete_result[i + len(insert_result)])):
#         CFCF.delete(delete_result[i + len(insert_result)][l])
#
#     CFCF_test_result.append(CFCF.size)
#
#     y2 = len(DCF_4) * DCF_4[0].capacity * 4
#     DCF_4_test_result.append(y2)
#
# print(" ")
# y2 = len(DCF_4) * DCF_4[0].capacity * 4
# print(y2)
# for i in range(len(DCF_4)):
#     print(DCF_4[i])
#
# import csv
#
# ##DCF_4_test_result
# # 1. 创建文件对象
# f = open('DCF_4_test_result.csv', 'w', encoding='utf-8', newline="")
# # 2. 基于文件对象构建 csv写入对象
# csv_writer = csv.writer(f)
# # 4. 写入csv文件内容
# for i in range(len(DCF_4_test_result)):
#     csv_writer.writerow([str(DCF_4_test_result[i])])
# # 5. 关闭文件
# f.close()
#
# ##DCF_4_test_result
# # 1. 创建文件对象
# f = open('CFCF_test_result.csv', 'w', encoding='utf-8', newline="")
# # 2. 基于文件对象构建 csv写入对象
# csv_writer = csv.writer(f)
# # 4. 写入csv文件内容
# for i in range(len(CFCF_test_result)):
#     csv_writer.writerow([str(CFCF_test_result[i])])
# # 5. 关闭文件
# f.close()

##开始存储
from Dynamic_cuckoo_filter import single_CF
import Dynamic_cuckoo_filter as CF_d_o

# 粒度为8个CF块的DCF
DCF_8 = single_CF(item_num=2 ** 15, fp=0.00048, exp_block_num=8)

DCF_8_test_result = []

for i in range(len(insert_result)):
    if insert_result[i] == "non" or len(insert_result[i]) == 0:
        print("non appear in insert_result", i)
        CF_d_o.dcf_delete(data=delete_result[i], sketch=DCF_8)
        CF_d_o.dcf_compact(sketch=DCF_8)

        x2 = len(DCF_8) * DCF_8[0].capacity * 4
        DCF_8_test_result.append(x2)

    else:
        # DCF_4
        CF_d_o.dcf_insert(data=insert_result[i], sketch=DCF_8)
        # for j in range(len(delete_result[i])):
        #     CF_d_o.dcf_delete(data=delete_result[i][j], sketch=DCF_4)
        CF_d_o.dcf_delete(data=delete_result[i], sketch=DCF_8)
        CF_d_o.dcf_compact(sketch=DCF_8)

        x2 = len(DCF_8) * DCF_8[0].capacity * 4
        DCF_8_test_result.append(x2)

for i in range(len(delete_result) - len(insert_result)):
    # DCF_4
    CF_d_o.dcf_delete(data=delete_result[i + len(insert_result)], sketch=DCF_8)
    CF_d_o.dcf_compact(sketch=DCF_8)

    y2 = len(DCF_8) * DCF_8[0].capacity * 4
    DCF_8_test_result.append(y2)

print(" ")
y2 = len(DCF_8) * DCF_8[0].capacity * 4
print(y2)
for i in range(len(DCF_8)):
    print(DCF_8[i])

import csv

##DCF_4_test_result
# 1. 创建文件对象
f = open('DCF_8_test_result.csv', 'w', encoding='utf-8', newline="")
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)
# 4. 写入csv文件内容
for i in range(len(DCF_8_test_result)):
    csv_writer.writerow([str(DCF_8_test_result[i])])
# 5. 关闭文件
f.close()
