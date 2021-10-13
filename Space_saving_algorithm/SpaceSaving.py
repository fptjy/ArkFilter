import math, heapq

from memory_profiler import profile
class SpaceSavingCounter:
    def __init__(self, eps):
        self.k = math.ceil(1 / eps)
        self.n = 0
        self.counts = dict()
        self.queue = []

    def inc(self, x):
        # increment total elements seen
        self.n += 1

        # x is being watched
        if x in self.counts:
            self.counts[x] += 1

        # x is not being watched
        else:
            # make room for x
            if self.n > self.k:
                while True:
                    count, tstamp, key = self.pop()
                    assert self.counts[key] >= count
                    if self.counts[key] == count:
                        del self.counts[key]
                        break
                    else:
                        self.push(self.counts[key], tstamp, key)
            else:
                count = 0

            # watch x
            self.counts[x] = count + 1
            self.push(count, self.n, x)

    def push(self, count, tstamp, key):
        heapq.heappush(
            self.queue,
            (count, tstamp, key)
        )

    def pop(self):
        return heapq.heappop(self.queue)


def test_SpaceSavingCounter():
    seq = [1, 5, 3, 4, 2, 7, 7, 1, 3, 1, 3, 1, 3, 1, 3]
    counter = SpaceSavingCounter(1 / 1.9)
    for x in seq:
        counter.inc(x)
    assert counter.counts.keys() == {1, 3}

# import random
# stream = ''
# for i, c in enumerate('abcdefghi', 1):
#     stream += c * 2 ** i
# stream = list(stream)
# print(stream)
# random.shuffle(stream)
# print(stream)
#
# seq = stream
# print(len(stream))
# seq = ["1", "5", "3", "4", "2", "7", "7", "1", "3", "1", "3", "1", "3", "1", "3"]
# counter = SpaceSavingCounter(1 / 2)
# for x in seq:
#     counter.inc(x)
# # assert counter.counts.keys() == {1, 3}
# print(counter.counts.keys())
# print(counter.counts.values())
# print(counter.counts.items())
#
# for x in counter.counts.keys():
#     print(x)
#     print(type(x))
#
# for x in counter.counts.values():
#     print(x)
#     print(type(x))

#
# print(counter.k)