import sys
sys.path.append("C:/Users/fptjy/pybloom")

from pybloom import BloomFilter
import bitarray, math
import datetime
from utils import range_fn
import random

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter

sys.path.append("C:/Users/fptjy/ArkFilter")
from Ark_Filter import Ark_Filter
import math
import numpy as np

from quotient_filter import QuotientFilter

# x = math.log2(8*0.95*100000)
# print(x)
# alpha_array = np.arange(0.025, 1, 0.05)
# print(alpha_array)
# print(len(alpha_array))

positive_lookup_BF = []
positive_lookup_CF = []
positive_lookup_ArkF = []
positive_lookup_QF = []

negative_lookup_BF = []
negative_lookup_CF = []
negative_lookup_ArkF = []
negative_lookup_QF = []

delete_CF = []
delete_ArkF = []
delete_QF = []

cishu = 30
for cs in range(cishu):

    #测试插入随机字符串
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
    testdata = [0 for i in range(2 ** 20)]
    for num in range(2 ** 20):
        sa = []
        for i in range(16):
            sa.append(random.choice(alphabet))
        testdata[num] = "".join(sa)

    testdata1 = [0 for i in range(2 ** 20)]
    for num in range(2 ** 20):
        sa = []
        for i in range(17):
            sa.append(random.choice(alphabet))
        testdata1[num] = "".join(sa)

    # 由于quotientfilter数量少，时间太短，分母为零报错，因此分开测试

    # 参数设置
    alpha_array = [0.025, 0.075, 0.125, 0.175]
    for j in range(len(alpha_array)):
        alpha = alpha_array[j]

        print("##########################################")
        print("##########################################")
        print("##########################################")
        print("table occupancy:", alpha)

        # 设置随机查询存在对象的数据集合
        datasize = int(alpha * len(testdata))
        testdata2 = [0 for i in range(datasize)]
        for i in range(datasize):
            testdata2[i] = testdata[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        """Test performance of BloomFilter at a set capacity and error rate."""
        print("Test performance of BloomFilter")
        f = BloomFilter(capacity=2 ** 20, error_rate=0.000015)
        # print("BF capacity:", f.capacity)
        request_error_rate = 0.00001
        start = datetime.datetime.now()
        for i in range_fn(int(alpha * len(testdata))):
            f.add(testdata[i], skip_check=True)
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata)) / time_consume))
        oneBits = f.bitarray.count(True)
        zeroBits = f.bitarray.count(False)
        # print "Number of 1 bits:", oneBits
        # print "Number of 0 bits:", zeroBits
        print("Number of Filter Bits:", f.num_bits)
        print("Number of slices:", f.num_slices)
        print("Bits per slice:", f.bits_per_slice)
        print("------")
        print("Fraction of 1 bits at capacity: {:5.3f}".format(
            oneBits / float(f.num_bits)))
        # Look for false positives and measure the actual fp rate
        trials = int(alpha * len(testdata))

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if f.__contains__(testdata1[i]):
                fp += 1
        print("Requested FP rate: {:2.4f}".format(request_error_rate))
        print("Experimental false positive rate: {:2.4f}".format(fp / trials))

        # 测试查询不存在的对象
        start = datetime.datetime.now()
        for i in range(trials):
            f.__contains__(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print(("{:5.3f} seconds to check 100% none-existed items, "
               "{:10.2f} checks/second".format(time_consume, trials / time_consume)))
        negative_lookup_BF.append(trials / time_consume)

        # 测试随机查询存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            f.__contains__(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print(("{:5.3f} seconds to check 100% existed items, "
               "{:10.2f} checks/second".format(time_consume, len(testdata2) / time_consume)))
        positive_lookup_BF.append(len(testdata2) / time_consume)

        # Compute theoretical fp max (Goel/Gupta)
        k = f.num_slices
        m = f.num_bits
        n = f.capacity
        fp_theory = math.pow((1 - math.exp(-k * (n + 0.5) / (m - 1))), k)
        print("Projected FP rate (Goel/Gupta): {:2.6f}".format(fp_theory))

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of CuckooFilter ")
        """Test performance of CuckooFilter at a set capacity and error rate."""
        cf = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19)

        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata))):
            cf.insert(testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, cf.size / time_consume))

        print("对象的平均bit数：", cf.fingerprint_size * cf.capacity * cf.bucket_size / cf.size)

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if cf.contains(testdata1[i]):
                fp += 1
        print("fp rate:", fp / int(alpha * len(testdata1)))

        # 查不存在的对象
        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata1))):
            cf.contains(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata1)) / time_consume))
        negative_lookup_CF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            cf.contains(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        positive_lookup_CF.append(len(testdata2) / time_consume)

        # 删除对象测试
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            cf.delete(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to delet , {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        delete_CF.append(len(testdata2) / time_consume)

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of ArkFilter")

        """Test performance of ArkFilter at a set capacity and error rate."""

        ARK = Ark_Filter(capacity=2 ** 18)

        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata))):
            ARK.insert(testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, ARK.size / time_consume))

        print("对象的平均bit数：", ARK.capacity * ARK.bucket_size / ARK.size * math.log2(ARK.capacity) / 2 + 1)

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if ARK.contains(testdata1[i]):
                fp += 1
        print("fp rate:", fp / int(alpha * len(testdata1)))

        # 查不存在的对象
        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata1))):
            ARK.contains(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata1)) / time_consume))
        negative_lookup_ArkF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            ARK.contains(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        positive_lookup_ArkF.append(len(testdata2) / time_consume)

        # 测试删除对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            ARK.delete(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to delet , {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        delete_ArkF.append(len(testdata2) / time_consume)

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of QuotientFilter")

        """Test performance of QuotientFilter at a set capacity and error rate."""

        qf = QuotientFilter()

        _testdata = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata[i] = testdata[i]

        _testdata1 = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata1[i] = testdata1[i]

        _testdata2 = [0 for i in range(int(alpha * qf.p))]
        for i in range(int(alpha * qf.p)):
            _testdata2[i] = _testdata[i]
        state = np.random.get_state()
        np.random.shuffle(_testdata2)
        np.random.set_state(state)

        num_size = int(alpha * len(_testdata))
        # 插入对象
        start = datetime.datetime.now()
        for j in range(10):
            for i in range(num_size):
                qf.addKey(_testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume / 10, num_size * 10 / time_consume))

        print("对象的平均bit数：", qf.r / alpha + 3)

        fp = 0
        for i in range(num_size):
            if qf.lookup(_testdata1[i]):
                fp += 1
        print("fp rate:", fp / num_size)

        # 查不存在的对象
        start = datetime.datetime.now()
        for j in range(10):
            for i in range(num_size):
                qf.lookup(_testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume / 10, num_size * 10 / time_consume))
        negative_lookup_QF.append(num_size * 10 / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for j in range(10):
            for i in range(len(_testdata2)):
                qf.lookup(_testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume / 10, len(_testdata2) * 10 / time_consume))
        positive_lookup_QF.append(len(_testdata2) * 10 / time_consume)

        # 测试删除对象
        start = datetime.datetime.now()
        for i in range(len(_testdata2)):
            qf.delete(_testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        print(time_s)
        print(time_ms)

        time_consume = time_s * 10 ** 6 + time_ms

        if time_consume == 0:
            delete_QF.append(0)
        else:
            delete_QF.append(len(_testdata2) * 10 ** 6 / time_consume)
        # print("{:5.3f} microseconds to delete existed item, {:10.2f} entries/microsecond".format(
        #     time_consume, len(_testdata2) / time_consume))
        # delete_QF.append(len(_testdata2) * 10 ** 6 / time_consume)

    # 正常测试
    # 参数设置
    alpha_array = np.arange(0.225, 1, 0.05)
    for j in range(len(alpha_array)):
        alpha = alpha_array[j]

        print("##########################################")
        print("##########################################")
        print("##########################################")
        print("table occupancy:", alpha)

        # 设置随机查询存在对象的数据集合
        datasize = int(alpha * len(testdata))
        testdata2 = [0 for i in range(datasize)]
        for i in range(datasize):
            testdata2[i] = testdata[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        """Test performance of BloomFilter at a set capacity and error rate."""
        print("Test performance of BloomFilter")
        f = BloomFilter(capacity=2 ** 20, error_rate=0.000015)
        # print("BF capacity:", f.capacity)
        request_error_rate = 0.000015
        start = datetime.datetime.now()
        for i in range_fn(int(alpha * len(testdata))):
            f.add(testdata[i], skip_check=True)
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata)) / time_consume))
        oneBits = f.bitarray.count(True)
        zeroBits = f.bitarray.count(False)
        # print "Number of 1 bits:", oneBits
        # print "Number of 0 bits:", zeroBits
        print("Number of Filter Bits:", f.num_bits)
        print("Number of slices:", f.num_slices)
        print("Bits per slice:", f.bits_per_slice)
        print("------")
        print("Fraction of 1 bits at capacity: {:5.3f}".format(
            oneBits / float(f.num_bits)))
        # Look for false positives and measure the actual fp rate
        trials = int(alpha * len(testdata))

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if f.__contains__(testdata1[i]):
                fp += 1
        print("Requested FP rate: {:2.4f}".format(request_error_rate))
        print("Experimental false positive rate: {:2.4f}".format(fp / trials))

        # 测试查询不存在的对象
        start = datetime.datetime.now()
        for i in range(trials):
            f.__contains__(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print(("{:5.3f} seconds to check 100% none-existed items, "
               "{:10.2f} checks/second".format(time_consume, trials / time_consume)))
        negative_lookup_BF.append(trials / time_consume)

        # 测试随机查询存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            f.__contains__(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print(("{:5.3f} seconds to check 100% existed items, "
               "{:10.2f} checks/second".format(time_consume, len(testdata2) / time_consume)))
        positive_lookup_BF.append(len(testdata2) / time_consume)

        # Compute theoretical fp max (Goel/Gupta)
        k = f.num_slices
        m = f.num_bits
        n = f.capacity
        fp_theory = math.pow((1 - math.exp(-k * (n + 0.5) / (m - 1))), k)
        print("Projected FP rate (Goel/Gupta): {:2.6f}".format(fp_theory))

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of CuckooFilter ")
        """Test performance of CuckooFilter at a set capacity and error rate."""
        cf = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19)

        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata))):
            cf.insert(testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, cf.size / time_consume))

        print("对象的平均bit数：", cf.fingerprint_size * cf.capacity * cf.bucket_size / cf.size)

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if cf.contains(testdata1[i]):
                fp += 1
        print("fp rate:", fp / int(alpha * len(testdata1)))

        # 查不存在的对象
        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata1))):
            cf.contains(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata1)) / time_consume))
        negative_lookup_CF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            cf.contains(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        positive_lookup_CF.append(len(testdata2) / time_consume)

        # 删除对象测试
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            cf.delete(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to delet , {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        delete_CF.append(len(testdata2) / time_consume)

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of ArkFilter")

        """Test performance of ArkFilter at a set capacity and error rate."""

        ARK = Ark_Filter(capacity=2 ** 18)

        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata))):
            ARK.insert(testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, ARK.size / time_consume))

        print("对象的平均bit数：", ARK.capacity * ARK.bucket_size / ARK.size * math.log2(ARK.capacity) / 2 + 1)

        fp = 0
        for i in range(int(alpha * len(testdata1))):
            if ARK.contains(testdata1[i]):
                fp += 1
        print("fp rate:", fp / int(alpha * len(testdata1)))

        # 查不存在的对象
        start = datetime.datetime.now()
        for i in range(int(alpha * len(testdata1))):
            ARK.contains(testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume, int(alpha * len(testdata1)) / time_consume))
        negative_lookup_ArkF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            ARK.contains(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        positive_lookup_ArkF.append(len(testdata2) / time_consume)

        # 测试删除对象
        start = datetime.datetime.now()
        for i in range(len(testdata2)):
            ARK.delete(testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to delet , {:10.2f} entries/second".format(
            time_consume, len(testdata2) / time_consume))
        delete_ArkF.append(len(testdata2) / time_consume)

        print("------------------------------------------")
        print("------------------------------------------")

        print("Test performance of QuotientFilter")

        """Test performance of QuotientFilter at a set capacity and error rate."""

        qf = QuotientFilter()

        _testdata = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata[i] = testdata[i]

        _testdata1 = [0 for i in range(qf.p)]
        for i in range(qf.p):
            _testdata1[i] = testdata1[i]

        _testdata2 = [0 for i in range(int(alpha * qf.p))]
        for i in range(int(alpha * qf.p)):
            _testdata2[i] = _testdata[i]
        state = np.random.get_state()
        np.random.shuffle(_testdata2)
        np.random.set_state(state)

        num_size = int(alpha * len(_testdata))
        # 插入对象
        start = datetime.datetime.now()
        for i in range(num_size):
            qf.addKey(_testdata[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
            time_consume, num_size / time_consume))

        print("对象的平均bit数：", qf.r / alpha + 3)

        fp = 0
        for i in range(num_size):
            if qf.lookup(_testdata1[i]):
                fp += 1
        print("fp rate:", fp / num_size)

        # 查不存在的对象
        start = datetime.datetime.now()
        for i in range(num_size):
            qf.lookup(_testdata1[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up none_existed item, {:10.2f} entries/second".format(
            time_consume, num_size / time_consume))
        negative_lookup_QF.append(num_size / time_consume)

        # 随机查存在的对象
        start = datetime.datetime.now()
        for i in range(len(_testdata2)):
            qf.lookup(_testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to look up existed item, {:10.2f} entries/second".format(
            time_consume, len(_testdata2) / time_consume))
        positive_lookup_QF.append(len(_testdata2) / time_consume)

        # 测试删除对象
        start = datetime.datetime.now()
        for i in range(len(_testdata2)):
            qf.delete(_testdata2[i])
        end = datetime.datetime.now()
        time_ms = (end - start).microseconds
        time_s = (end - start).seconds
        time_consume = time_s + time_ms / 10 ** 6
        print("{:5.3f} seconds to delete existed item, {:10.2f} entries/second".format(
            time_consume, len(_testdata2) / time_consume))
        delete_QF.append(len(_testdata2) / time_consume)

positive_lookup_BF2 = [0 for i in range(20)]
positive_lookup_CF2 = [0 for i in range(20)]
positive_lookup_ArkF2 = [0 for i in range(20)]
positive_lookup_QF2 = [0 for i in range(20)]

negative_lookup_BF2 = [0 for i in range(20)]
negative_lookup_CF2 = [0 for i in range(20)]
negative_lookup_ArkF2 = [0 for i in range(20)]
negative_lookup_QF2 = [0 for i in range(20)]

delete_CF2 = [0 for i in range(20)]
delete_ArkF2 = [0 for i in range(20)]
delete_QF2 = [0 for i in range(20)]

for j in range(20):
    k = j
    for i in range(cishu):
        negative_lookup_BF2[j] += negative_lookup_BF[k]
        negative_lookup_CF2[j] += negative_lookup_CF[k]
        negative_lookup_ArkF2[j] += negative_lookup_ArkF[k]
        negative_lookup_QF2[j] += negative_lookup_QF[k]

        positive_lookup_BF2[j] += positive_lookup_BF[k]
        positive_lookup_CF2[j] += positive_lookup_CF[k]
        positive_lookup_ArkF2[j] += positive_lookup_ArkF[k]
        positive_lookup_QF2[j] += positive_lookup_QF[k]

        delete_CF2[j] += delete_CF[k]
        delete_ArkF2[j] += delete_ArkF[k]
        delete_QF2[j] += delete_QF[k]
        k += 20

count = [0 for i in range(20)]
for j in range(20):
    k = j
    for i in range(cishu):
        if delete_QF[k] == 0:
            count[j] += 1
            k += 20

print("count为：", count)


for i in range(20):
    negative_lookup_BF2[i] = negative_lookup_BF2[i] / cishu
    negative_lookup_CF2[i] = negative_lookup_CF2[i] / cishu
    negative_lookup_ArkF2[i] = negative_lookup_ArkF2[i] / cishu
    negative_lookup_QF2[i] = negative_lookup_QF2[i] / cishu

    positive_lookup_BF2[i] = positive_lookup_BF2[i] / cishu
    positive_lookup_CF2[i] = positive_lookup_CF2[i] / cishu
    positive_lookup_ArkF2[i] = positive_lookup_ArkF2[i] / cishu
    positive_lookup_QF2[i] = positive_lookup_QF2[i] / cishu

    delete_CF2[i] = delete_CF2[i] / cishu
    delete_ArkF2[i] = delete_ArkF2[i] / cishu
    delete_QF2[i] = delete_QF2[i] / (cishu - count[i])





print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("打印实验结果")

print("negative_lookup_BF2", negative_lookup_BF2)
print("negative_lookup_CF2", negative_lookup_CF2)
print("negative_lookup_ArkF2", negative_lookup_ArkF2)
print("negative_lookup_QF2", negative_lookup_QF2)

print("positive_lookup_BF2", positive_lookup_BF2)
print("positive_lookup_CF2", positive_lookup_CF2)
print("positive_lookup_ArkF2", positive_lookup_ArkF2)
print("positive_lookup_QF2", positive_lookup_QF2)

print("delete_CF2", delete_CF2)
print("delete_ArkF2", delete_ArkF2)
print("delete_QF2", delete_QF2)