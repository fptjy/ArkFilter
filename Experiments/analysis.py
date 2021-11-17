import math
# encoding=utf-8
import matplotlib

matplotlib.rcParams["backend"] = "SVG"
import numpy as np
import matplotlib.pyplot as plt

def space_AF(n, alpha, b):
    capacity = math.ceil(n / alpha)
    ma = math.ceil(capacity / b)
    space = ma * b * (math.ceil(math.log(ma, 2)) + 1)
    return space / n


def space_CF(n, alpha, b):
    capacity = math.ceil(n / alpha)
    ma = math.ceil(capacity / b)
    mcf = 2 ** math.ceil(math.log(ma, 2))
    space = mcf * b * (math.ceil(math.log(ma - 1, 2)) + 1)
    return space / n


N = [i for i in range(2 ** 10, 2 ** 20 + 1)]

AF = []
CF = []
for i in N:
    AF.append(space_AF(i, 0.95, 4))
    CF.append(space_CF(i, 0.95, 4))


y1 = np.array(AF)
y2 = np.array(CF)


fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=100)
# 设置自变量的范围和个数
# x = np.arange(0.025, 1, 0.05)

x = np.linspace(0, len(N), y2.shape[0])
for i in range(len(x)):
    x[i] = x[i] / 10 ** 6

# 画图
# ax.plot(x, y_1, label='Optimum', linestyle=':', color="black")
ax.plot(x, y1, label='AF', linestyle='-', color="crimson")
ax.plot(x, y2, label='CF', linestyle='--', color="steelblue")
# ax.plot(x, y_3, label='DCF1', linestyle='--', color="crimson")
# ax.plot(x, y_4, label='DAF', linestyle='-', color="crimson")
# ax.plot(x, y_5, label='Dynamic VCF', linestyle='-', color="steelblue")
# ax.plot(x, y1, label='BF', linestyle='--', marker='*', color="steelblue", markersize='8')
# ax.plot(x, y2, label='CF', linestyle='--', marker='o', color="darkorange", markersize='8')
# ax.plot(x, y3, label='ArkF', linestyle='--', marker='v', color="crimson", markersize='8')
# ax.plot(x, y4, label='QF', linestyle='--', marker='d', color="mediumseagreen", markersize='8')
# 设置坐标轴
# ax.set_xlim(0, 9.5)
# ax.set_ylim(0, 12)
ax.set_xlabel('number of elements ($×$10$^6$)', fontdict={"family": "Times New Roman", "weight": "normal", "size": 19})
ax.set_ylabel('bpe',
              fontdict={"family": "Times New Roman", "weight": "normal", "size": 19})
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
legend = ax.legend(loc="best", prop={'family': 'Times New Roman', "size": 14})

plt.show()

# fig.savefig('C:/Users/fptjy/Desktop/Quotient CF/实验结果/bpe_vs_size.svg', dpi=600, format='svg')