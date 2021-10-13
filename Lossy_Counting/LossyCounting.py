# LossyCounting通过对数据流进行划分窗口，每个窗口统计后都对频数减1，最终保存下来的元素，都是频数超过N*epsilon的元素
class LossyCounting(object):
    def __init__(self, epsilon):
        self.N = 0
        self.count = {}
        self.bucketID = {}
        self.epsilon = epsilon
        self.b_current = 1
        self.del_number = 0
        self.add_new_number = 0

    def getCount(self, item):
        return self.count[item]

    def getBucketID(self, item):
        return self.bucketID[item]

    def trim(self):
        for item in list(self.count.keys()):
            if self.count[item] <= self.b_current - self.bucketID[item]:
                self.del_number += 1
                del self.count[item]
                del self.bucketID[item]

    def addCount(self, item):
        self.N += 1
        if item in self.count:
            self.count[item] += 1
        else:
            self.add_new_number += 1
            self.count[item] = 1
            self.bucketID[item] = self.b_current - 1


        if self.N % int(1 / self.epsilon) == 0:
            self.trim()
            self.b_current += 1

    def iterateOverThresholdCount(self, threshold_count):
        # assert threshold_count > self.epsilon * self.N, "too small threshold"

        self.trim()
        for item in self.count:
            if self.count[item] >= threshold_count - self.epsilon * self.N:
                yield (item, self.count[item])

    def iterateOverThresholdRate(self, threshold_rate):
        return self.iterateOverThresholdCount(threshold_rate * self.N)

# if __name__ == '__main__':
#     import random
#
#     counter = LossyCounting(5e-3)
#
#     stream = ''
#     for i, c in enumerate('abcdefghi', 1):
#         stream += c * 2 ** i
#     stream = list(stream)
#     print(stream)
#     random.shuffle(stream)
#     print(stream)
#
#     for c in stream:
#         counter.addCount(c)
#
#     for item, count in sorted(counter.iterateOverThresholdCount(10), key=lambda x: x[1]):
#         if count > 100:
#             print(item, count)
