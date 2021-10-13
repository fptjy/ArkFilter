from MinHeap import MinHeap
import numpy as np
from HeavyKeeper import HeavyKeeperSketch
import random
import math



###测试HeavyKeeper
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
number = 1024-5
testdata = [0 for i in range(number)]
for num in range(number):
    sa = []
    for i in range(4):
        sa.append(random.choice(alphabet))
    testdata[num] = "".join(sa)

print(testdata)
testdata.append("s")
testdata.append("ss")
testdata.append("sss")
testdata.append("ssss")
testdata.append("sssss")

##指数分布##
np.random.seed(3)
x3 = np.random.exponential(20, size=number)
y3 = []
for i in range(len(x3)):
    z = math.ceil(x3[i])
    if z >= 1:
        y3.append(z)
    else:
        y3.append(1)
y3.append(270)
y3.append(300)
y3.append(350)
y3.append(400)
y3.append(360)


print(y3)
print(x3.max())
print(len(testdata))
print(len(y3))

final_data = []
for i in range(len(testdata)):
    for j in range(y3[i]):
        final_data.append(testdata[i])

# print(len(final_data))
# print(final_data)

np.random.shuffle(final_data)
# print(final_data)

MinHeap = MinHeap(7)
HKS = HeavyKeeperSketch(width=256, depth=4, seeds=[0, 1, 2, 3], finger_size=2 ** 8, base=1.08)

for i in range(len(final_data)):
    HKS.insert(final_data[i])

for i in range(len(testdata)):
    lookup = HKS.query(testdata[i])
    MinHeap.heavy_keep(testdata[i], lookup)

for i in range(MinHeap.maxsize):
    print(MinHeap._elements[i])


print(HKS.query("s"))
print(HKS.query("ss"))
print(HKS.query("sss"))
print(HKS.query("ssss"))
print(HKS.query("sssss"))