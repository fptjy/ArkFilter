import random
from Ark_Filter import Ark_Filter
import time

# 测试插入随机字符串
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
AF_size = 1024*4
size = 1024
testdata = [0 for i in range(AF_size)]
for num in range(AF_size):
    sa = []
    for i in range(16):
        sa.append(random.choice(alphabet))
    testdata[num] = "".join(sa)

testdata1 = [0 for i in range(AF_size)]
for num in range(AF_size):
    sa = []
    for i in range(17):
        sa.append(random.choice(alphabet))
    testdata1[num] = "".join(sa)


ARK = Ark_Filter(capacity=size)

alpha = 0.95
print(int(alpha*len(testdata)))

start = time.time()
for i in range(int(alpha*len(testdata))):
    ARK.insert(testdata[i])
end = time.time()
print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
    end - start, ARK.size / (end - start)))

print(ARK.size)

print(ARK.buckets[0])
print(ARK.buckets[1])
print(ARK.buckets[2])
