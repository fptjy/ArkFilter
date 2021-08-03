# encoding=utf-8
import matplotlib
from collections import Counter

matplotlib.rcParams["backend"] = "SVG"
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

# 输入因变量

##第二个图，关于Dvcf的
# 输入因变量

# x = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
OS2ECTM = [0.55, 0.578, 0.62, 0.632, 0.653, 0.643, 0.66, 0.628, 0.64, 0.645, 0.652]

SECM = [0.357, 0.375, 0.382, 0.335, 0.36, 0.41, 0.368, 0.36, 0.376, 0.382, 0.372]

ICMT = [0.523, 0.57, 0.545, 0.568, 0.552, 0.558, 0.58, 0.552, 0.527, 0.55, 0.51]

Spray10 = [0.413, 0.432, 0.423, 0.472, 0.42, 0.442, 0.462, 0.415, 0.43, 0.428, 0.463]

Spray30 = [0.325, 0.375, 0.358, 0.335, 0.32, 0.37, 0.34, 0.323, 0.358, 0.352, 0.368]

BubbleRap = [0.532, 0.557, 0.62, 0.633, 0.642, 0.649, 0.652, 0.617, 0.641, 0.638, 0.657]

SimBet = [0.489, 0.528, 0.536, 0.61, 0.628, 0.634, 0.629, 0.589, 0.637, 0.625, 0.617]

y1 = np.array(OS2ECTM)
y2 = np.array(SECM)
y3 = np.array(ICMT)
y4 = np.array(Spray10)
y5 = np.array(Spray30)
y6 = np.array(BubbleRap)
y7 = np.array(SimBet)

# assert y1.shape[0]==y2.shape[0], '两个因变量个数不相等！'
fig, ax = plt.subplots(figsize=(7.7, 4.2), dpi=100)
# 设置自变量的范围和个数
x = np.linspace(1, 6, len(SECM))
# 画图
ax.plot(x, y1, label='OS2ECTM', linestyle='-', marker='^', markersize='6')
ax.plot(x, y2, label='SECM', linestyle='-', marker='D', markersize='6')
ax.plot(x, y3, label='ICMT', linestyle='-', marker='v', markersize='6')
ax.plot(x, y4, label='Spray10', linestyle='-', marker='s', markersize='6')
ax.plot(x, y5, label='Spray30', linestyle='-', marker='<', markersize='6')
ax.plot(x, y6, label='BubbleRap', linestyle='-', marker='o', markersize='6')
ax.plot(x, y7, label='SimBet', linestyle='-', marker='>', markersize='6')

# ax.plot(x, y8, label='DVCF7', linestyle='-.', marker='s', markersize='8')
# ax.plot(x, y9, label='DVCF8', linestyle='-', marker='*', markersize='8')
# ax.plot(x, y10, label='D-ary CF', linestyle='-', marker='+', markersize='8')

# 设置坐标轴
# ax.set_xlim(0, 9.5)
# ax.set_ylim(0, 1.4)
# ax.set_xlabel('filter size()')
# ax.set_ylabel('distance(m)')
ax.set_xlabel('time/h', fontdict={"family": "Times New Roman", "weight": "normal", "size": 16})
ax.set_ylabel('Delivery ratio', fontdict={"family": "Times New Roman", "weight": "normal", "size": 16})
# 设置刻度
ax.tick_params(labelsize=16)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
# 显示网格
# ax.grid(True, linestyle='-.')
ax.yaxis.grid(True, linestyle='-.')
# 添加图例
legend = ax.legend(bbox_to_anchor=(1.02, 0.43), loc=3, borderaxespad=0, prop={'family': 'Times New Roman', "size": 13})

plt.show()
# fig.savefig('C:/Users/fptjy/Desktop/lpbb.svg', dpi=600, format='svg')
# fig.savefig('1.png')
