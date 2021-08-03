# # encoding=utf-8
# import matplotlib
#
# matplotlib.rcParams["backend"] = "SVG"
# import numpy as np
# import matplotlib.pyplot as plt
# import math
# import pandas as pd
#
# # 输入因变量
#
#
# """
# #Read data
# """
# CFCF_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/CFCF_test_result.csv', 'r') as fin:
#     for line in fin:
#         CFCF_test_result.append(int(line.replace("\n", "")))
# fin.close()
#
# DCF_4_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/DCF_4_test_result.csv', 'r') as fin:
#     for line in fin:
#         DCF_4_test_result.append(int(line.replace("\n", "")))
# fin.close()
#
# DCF_8_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/DCF_8_test_result.csv', 'r') as fin:
#     for line in fin:
#         DCF_8_test_result.append(int(line.replace("\n", "")))
# fin.close()
#
# DAF_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/ArkFilter_for_Dynamics/DAF_test_result.csv', 'r') as fin:
#     for line in fin:
#         DAF_test_result.append(int(line.replace("\n", "")))
# fin.close()
#
# DVCF_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/VCF_for_Dynamics/DVCF_test_result.csv', 'r') as fin:
#     for line in fin:
#         DVCF_test_result.append(int(line.replace("\n", "")))
# fin.close()
#
# y1 = np.array(CFCF_test_result)
# y2 = np.array(DCF_4_test_result)
# y3 = np.array(DCF_8_test_result)
# y4 = np.array(DAF_test_result)
# y5 = np.array(DVCF_test_result)
#
# fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=100)
# # 设置自变量的范围和个数
# # x = np.arange(0.025, 1, 0.05)
#
# x = np.linspace(0, len(CFCF_test_result), y1.shape[0])
# for i in range(len(x)):
#     x[i] = x[i] / 10**4
#
# y_1 = []
# y_2 = []
# y_3 = []
# y_4 = []
# y_5 = []
#
# for i in range(len(y2)):
#     y_2.append(y2[i] / 10**4)
# for i in range(len(y5)):
#     y_5.append(y5[i] / 10**4)
# for i in range(len(y1)):
#     y_1.append(y1[i] / 10**4)
# for i in range(len(y3)):
#     y_3.append(y3[i] / 10**4)
# for i in range(len(y4)):
#     y_4.append(y4[i] / 10**4)
#
#
# # 画图
# ax.plot(x, y_1, label='Optimum', linestyle=':', color="black")
# ax.plot(x, y_2, label='DCF_4', linestyle='-.', color="darkorange")
# ax.plot(x, y_3, label='DCF_8', linestyle='--', color="steelblue")
# ax.plot(x, y_4, label='DAF', linestyle='-', color="crimson")
# # ax.plot(x, y_5, label='DVCF', linestyle='-', color="steelblue")
# # 设置坐标轴
# # ax.set_xlim(0, 9.5)
# # ax.set_ylim(0, 5)
# ax.set_xlabel('time ($×$ 10$^4$ ms)', fontdict={"family": "Times New Roman", "weight": "normal", "size": 18})
# ax.set_ylabel('capacity of filter ($×$ 10$^4$)', fontdict={"family": "Times New Roman", "weight": "normal", "size": 18})
# # plt.xlabel("f: fingerprint size in bits", fontdict=) log$_{10}$ξ$^‘$
# # 设置刻度
# # ax.tick_params(axis='both')
# ax.tick_params(labelsize=16)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# # 显示网格
# # ax.grid(True, linestyle='-.')
# ax.yaxis.grid(True, linestyle='-.')
# # 添加图例
# legend = ax.legend(loc='best', prop={'family': 'Times New Roman', "size": 14})
#
# plt.show()
#
# fig.savefig('C:/Users/fptjy/Desktop/Quotient CF/实验结果/dynamic_test_AF1.svg', dpi=600, format='svg')
# # # fig.savefig('1.png')   #保存图片


# encoding=utf-8
import matplotlib
from collections import Counter

matplotlib.rcParams["backend"] = "SVG"
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

# 输入因变量


"""
#Read data
"""
# CFCF_test_result = []
# with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/CFCF_test_result.csv', 'r') as fin:
#     for line in fin:
#         CFCF_test_result.append(int(line.replace("\n", "")))
# fin.close()

DCF_4_test_result = []
with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/DCF_4_test_result.csv', 'r') as fin:
    for line in fin:
        DCF_4_test_result.append(int(line.replace("\n", "")))
fin.close()

def process_rawdata(DCF_4_test_result):
    dict1 = Counter(DCF_4_test_result)

    DCF_4_test_result2 = []
    for item in dict1.items():
        DCF_4_test_result2.append([item[0], item[1]])

    DCF_4_test_result3 = sorted(DCF_4_test_result2, key=(lambda x: x[0]))

    print(DCF_4_test_result3)

    total_time = 0
    for i in range(len(DCF_4_test_result3)):
        total_time += DCF_4_test_result3[i][1]
    DCF_4_test_result_y = [0 for i in range(len(DCF_4_test_result3))]
    for i in range(len(DCF_4_test_result3)):
        DCF_4_test_result_y[i] = DCF_4_test_result_y[i - 1] + DCF_4_test_result3[i][1] / total_time
    return DCF_4_test_result_y


DCF_4_test_result_y = process_rawdata(DCF_4_test_result)
print(DCF_4_test_result_y)

DCF_8_test_result = []
with open('C:/Users/fptjy/ArkFilter_experiment/Dynamic_CF/DCF_8_test_result.csv', 'r') as fin:
    for line in fin:
        DCF_8_test_result.append(int(line.replace("\n", "")))
fin.close()

DCF_8_test_result_y = process_rawdata(DCF_8_test_result)
print(DCF_8_test_result_y)

DAF_test_result = []
with open('C:/Users/fptjy/ArkFilter_experiment/ArkFilter_for_Dynamics/DAF_test_result.csv', 'r') as fin:
    for line in fin:
        DAF_test_result.append(int(line.replace("\n", "")))
fin.close()

DAF_test_result_y = process_rawdata(DAF_test_result)
print(DAF_test_result_y)

DVCF_test_result = []
with open('C:/Users/fptjy/ArkFilter_experiment/VCF_for_Dynamics/DVCF_test_result.csv', 'r') as fin:
    for line in fin:
        DVCF_test_result.append(int(line.replace("\n", "")))
fin.close()

DVCF_test_result_y = process_rawdata(DVCF_test_result)
print(DVCF_test_result_y)

# y1 = np.array(CFCF_test_result)
y2 = np.array(DCF_4_test_result_y)
y3 = np.array(DCF_8_test_result_y)
y4 = np.array(DAF_test_result_y)
y5 = np.array(DVCF_test_result_y)

fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=100)
# 设置自变量的范围和个数
# x = np.arange(0.025, 1, 0.05)

x2 = np.linspace(0, 49152, len(y2))
x3 = np.linspace(0, 40960, len(y3))
x4 = np.linspace(0, 40960, len(y4))
x5 = np.linspace(0, 32768, len(y5))

for i in range(len(x2)):
    x2[i] = x2[i] / 10**4

for i in range(len(x3)):
    x3[i] = x3[i] / 10**4

for i in range(len(x4)):
    x4[i] = x4[i] / 10**4

for i in range(len(x5)):
    x5[i] = x5[i] / 10**4

# 画图
# ax.plot(x, y1, label='Benchmark', linestyle='-', color="black")
ax.plot(x2, y2, label='DCF_4', linestyle='-.', marker='o', color="darkorange", markersize='8')
ax.plot(x3, y3, label='DCF_8', linestyle='--', marker='v', color="steelblue", markersize='8')
ax.plot(x4, y4, label='DAF', linestyle='-', marker='d', color="crimson", markersize='8')
# ax.plot(x5, y5, label='DVCF', linestyle='-', marker='*', color="steelblue", markersize='8')
# ax.plot(x, y1, label='BF', linestyle='--', marker='*', color="steelblue", markersize='8')
# ax.plot(x, y2, label='CF', linestyle='--', marker='o', color="darkorange", markersize='8')
# ax.plot(x, y3, label='ArkF', linestyle='--', marker='v', color="crimson", markersize='8')
# ax.plot(x, y4, label='QF', linestyle='--', marker='d', color="mediumseagreen", markersize='8')
# 设置坐标轴
# ax.set_xlim(0, 9.5)
# ax.set_ylim(0, 1.4)
ax.set_xlabel('capacity of filter ($×$ 10$^4$)', fontdict={"family":"Times New Roman","weight": "normal", "size": 18})
ax.set_ylabel('CDF', fontdict={"family":"Times New Roman","weight": "normal", "size": 18})
# plt.xlabel("f: fingerprint size in bits", fontdict=) log$_{10}$ξ$^‘$
# 设置刻度
# ax.tick_params(axis='both')
ax.tick_params(labelsize=16)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
# 显示网格
# ax.grid(True, linestyle='-.')
ax.yaxis.grid(True, linestyle='-.')
# 添加图例
legend = ax.legend(loc='best', prop={'family': 'Times New Roman', "size": 14})

plt.show()

fig.savefig('C:/Users/fptjy/Desktop/Quotient CF/实验结果/dynamic_test_AF2.svg', dpi=600, format='svg')
# # fig.savefig('1.png')   #保存图片图片
