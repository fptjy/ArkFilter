# import sys
import random
# from pybloom import BloomFilter
# f = BloomFilter(capacity=1000, error_rate=0.001)
# print(sys.getsizeof(f))
# # f.add(x) for x in range(10)
# # all([(x in f) for x in range(10)])
#
# z =f.add(1)
# print(z)
# z=f.add(1)
# print(z)
# z=2 in f
# print(z)
# z= 1 in f
# print(z)
#
# # 测试插入16位的随机字符串
# alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
# testdata = [0 for i in range(2**22)]
# for num in range(2**22):
#     sa = []
#     for i in range(16):
#         sa.append(random.choice(alphabet))
#     testdata[num] = "".join(sa)
#
# a = BloomFilter(capacity=2**22, error_rate=0.001)
#
# print("a存储前的大小", sys.getsizeof(a))
#
# for i in range(len(testdata)):
#     a.add(testdata[i])
# print(a)
# print(a.count)
#
# print("a存储后的大小", sys.getsizeof(a))
#
# true_number = 0
# for i in range(len(testdata)):
#     if testdata[i] in a:
#         true_number += 1
#
# print("返回true的结果个数为:", true_number)
#
#
# alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
# testdata1 = [0 for i in range(2**22)]
# for num in range(2**22):
#     sa = []
#     for i in range(17,20):
#         sa.append(random.choice(alphabet))
#     testdata1[num] = "".join(sa)
#
# false_number = 0
# for i in range(len(testdata1)):
#     if testdata1[i] in a:
#         false_number += 1
#
# print("返回false的结果个数为:", false_number)


#!/usr/bin/env python
#

"""Test performance of BloomFilter at a set capacity and error rate."""
import sys
from pybloom import BloomFilter
import bitarray, math, time
from utils import range_fn
import random

# 测试插入随机字符串
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
testdata = [0 for i in range(2**20)]
for num in range(2**20):
    sa = []
    for i in range(16):
        sa.append(random.choice(alphabet))
    testdata[num] = "".join(sa)


testdata1 = [0 for i in range(2**20)]
for num in range(2**20):
    sa = []
    for i in range(17):
        sa.append(random.choice(alphabet))
    testdata1[num] = "".join(sa)

def main(capacity=2**20, request_error_rate=0.001):
    f = BloomFilter(capacity=capacity, error_rate=request_error_rate)
    assert (capacity == f.capacity)
    start = time.time()
    for i in range_fn(len(testdata)):
        f.add(testdata[i], skip_check=True)
    end = time.time()
    print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            end - start, f.capacity / (end - start)))
    oneBits = f.bitarray.count(True)
    zeroBits = f.bitarray.count(False)
    #print "Number of 1 bits:", oneBits
    #print "Number of 0 bits:", zeroBits
    print("Number of Filter Bits:", f.num_bits)
    print("Number of slices:", f.num_slices)
    print("Bits per slice:", f.bits_per_slice)
    print("------")
    print("Fraction of 1 bits at capacity: {:5.3f}".format(
            oneBits / float(f.num_bits)))
    # Look for false positives and measure the actual fp rate
    trials = f.capacity
    fp = 0
    start = time.time()
    for i in range(len(testdata1)):
        if f.__contains__(testdata1[i]):
            fp += 1
    end = time.time()
    print(("{:5.3f} seconds to check false positives, "
           "{:10.2f} checks/second".format(end - start, trials / (end - start))))
    print("Requested FP rate: {:2.4f}".format(request_error_rate))
    print("Experimental false positive rate: {:2.4f}".format(fp / float(trials)))
    # Compute theoretical fp max (Goel/Gupta)
    k = f.num_slices
    m = f.num_bits
    n = f.capacity
    fp_theory = math.pow((1 - math.exp(-k * (n + 0.5) / (m - 1))), k)
    print("Projected FP rate (Goel/Gupta): {:2.6f}".format(fp_theory))

if __name__ == '__main__' :
    status = main()
    sys.exit(status)

