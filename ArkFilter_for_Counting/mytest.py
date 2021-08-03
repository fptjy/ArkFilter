import random
from Counting_Ark_Filter import Counting_Ark_Filter
import time
import numpy as np
import math

# 测试插入随机字符串
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
size = 1024
AF_size = size*4
testdata = [0 for i in range(AF_size)]
for num in range(AF_size):
    sa = []
    for i in range(16):
        sa.append(random.choice(alphabet))
    testdata[num] = "".join(sa)

##实现正态分布的随机抽样##
np.random.seed(1)
x = np.random.normal(loc=30, scale=10, size=AF_size)
print(x)

y = []
for i in range(len(x)):
    z = math.ceil(x[i])
    if z >= 1:
        y.append(z)
    else:
        y.append(1)



ARK = Counting_Ark_Filter(capacity=size)

alpha = 0.95
print(int(alpha*len(testdata)))

start = time.time()
for i in range(int(alpha*len(testdata))):
    ARK.insert(testdata[i], y[i])
end = time.time()
print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
    end - start, ARK.size / (end - start)))

print(ARK.size)

print(ARK.buckets[0])
print(ARK.buckets[1])
print(ARK.buckets[2])

print(ARK.query(testdata[0]))
print(y[0])
