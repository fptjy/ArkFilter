# import math
#
# a = 0.95
# b = 1024
# f = 2*a/(b-1)
# print(f)
# z = (4 * a + 2 * f) / f
# bpe_NF = math.log(z, 2) / a
#
# print(bpe_NF)
#
# a = 0.95
# b1 = 2**2
# m1 = 2**10
# f1 = b1*a/(m1-1)
# print(f1)
# z1 = (2 * a * 4 + 2 * f1) / f1
# bpe_AF = math.log(z1, 2) / a
# print(bpe_AF)
#
#
# from __future__ import absolute_import
# import math
# import hashlib
# from utils import range_fn, is_string_io, running_python_3
# from struct import unpack, pack, calcsize
#
# try:
#     import bitarray
# except ImportError:
#     raise ImportError('pybloom requires bitarray >= 0.3.4')
#
# def make_hashfuncs(num_slices, num_bits):
#     if num_bits >= (1 << 31):
#         fmt_code, chunk_size = 'Q', 8
#     elif num_bits >= (1 << 15):
#         fmt_code, chunk_size = 'I', 4
#     else:
#         fmt_code, chunk_size = 'H', 2
#     total_hash_bits = 8 * num_slices * chunk_size
#     # if total_hash_bits > 384:
#     #     hashfn = hashlib.sha512
#     # elif total_hash_bits > 256:
#     #     hashfn = hashlib.sha384
#     # elif total_hash_bits > 160:
#     #     hashfn = hashlib.sha256
#     # elif total_hash_bits > 128:
#     #     hashfn = hashlib.sha1
#     # else:
#     #     hashfn = hashlib.md5
#
#     hashfn = hashlib.md5
#
#     fmt = fmt_code * (hashfn().digest_size // chunk_size)
#
#     # print(fmt)
#
#     num_salts, extra = divmod(num_slices, len(fmt))
#     # print("num_salts", num_salts)
#     # print(num_salts, extra)
#
#     if extra:
#         num_salts += 1
#     salts = tuple(hashfn(hashfn(pack('I', i)).digest()) for i in range_fn(num_salts))
#     # print(salts)
#
#     def _make_hashfuncs(key, hash_number=num_slices):
#         if running_python_3:
#             if isinstance(key, str):
#                 key = key.encode('utf-8')
#             else:
#                 key = str(key).encode('utf-8')
#         else:
#             if isinstance(key, unicode):
#                 key = key.encode('utf-8')
#             else:
#                 key = str(key)
#         i = 0
#         for salt in salts:
#             # print(salt)
#             h = salt.copy()
#             # print("h为", h)
#             h.update(key)
#             for uint in unpack(fmt, h.digest()):
#                 yield uint % num_bits
#                 i += 1
#                 if i >= hash_number:  #哈希结果的个数取决于这里
#                     return
#
#     return _make_hashfuncs
#
# x = make_hashfuncs(8, 2**25)
# print("hashes")
# hashes = x("sss")
# for i in hashes:
#     print(i)
# """
#
# """

# import math
# size = 2**18
# capacity = size*4
# m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(77, 2))))
# print("m", m)   #27278500
# print(math.log(m, 2))   #24.7


###test Adaptive_BF###
import sys
import numpy as np
import math
import random
import time
from Adaptive_BF import Adaptive_BloomFilter

#实验参数设置
cishu = 2

alpha = 0.95
size = 2**18
capacity = size*4

##实现正态分布的随机抽样##
np.random.seed(1)
x1 = np.random.normal(loc=30, scale=5, size=capacity)

y1 = []
for i in range(len(x1)):
    z = math.ceil(x1[i])
    if z >= 1:
        y1.append(z)
    else:
        y1.append(1)

for j in range(10):
    print(y1[j])

print("maxmium in y1", max(y1))

# 测试插入随机字符串
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
testdata = [0 for i in range(capacity)]
for num in range(capacity):
    sa = []
    for i in range(16):
        sa.append(random.choice(alphabet))
    testdata[num] = "".join(sa)

y = y1
#ABF使用4个哈希函数的实验
ABF4 = Adaptive_BloomFilter(k=4, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
start = time.time()
for i in range(int(alpha*len(testdata))):
    ABF4.insert(testdata[i], y[i])
end = time.time()
print("ABF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
    end - start, int(alpha*len(testdata)) / (end - start)))

for i in range(16):
    print(ABF4.query(testdata[i]), y[i])

print(ABF4.query("sss"))


# ###test SBF###
# import sys
# import numpy as np
# import math
# import random
# import time
# from Shifting_BF import Shifting_BloomFilter
#
# #实验参数设置
# cishu = 2
#
# alpha = 0.95
# size = 2**18
# capacity = size*4
#
# ##实现正态分布的随机抽样##
# np.random.seed(1)
# x1 = np.random.normal(loc=30, scale=10, size=capacity)
#
# y1 = []
# for i in range(len(x1)):
#     z = math.ceil(x1[i])
#     if z >= 1:
#         y1.append(z)
#     else:
#         y1.append(1)
#
# # 测试插入随机字符串
# alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
# testdata = [0 for i in range(capacity)]
# for num in range(capacity):
#     sa = []
#     for i in range(16):
#         sa.append(random.choice(alphabet))
#     testdata[num] = "".join(sa)
#
# y = y1
# #ABF使用4个哈希函数的实验
# SBF4 = Shifting_BloomFilter(k=4, m=math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))), max=max(y))
# print(math.ceil(capacity*(20.014804508959585+math.ceil(math.log(max(y), 2)))))
# start = time.time()
# for i in range(int(alpha*len(testdata))):
#     SBF4.insert(testdata[i], y[i])
# end = time.time()
# print("SBF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
#     end - start, int(alpha*len(testdata)) / (end - start)))
#
# for i in range(16):
#     print(SBF4.query(testdata[i]), y[i])
#
# print(SBF4.query("sss"))
# print(max(y))

