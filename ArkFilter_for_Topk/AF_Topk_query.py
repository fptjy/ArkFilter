import sys
import Topk_Ark_Filter
import math

sys.path.append(r"C:/Users/fptjy/ArkFilter_experiment/HeavyKeeper")
from MinHeap import MinHeap


# 最大堆的实现
class MaxHeap():
    def __init__(self, maxSize=None, filter_capacity=2 ** 20):
        self.maxSize = maxSize
        self.li = [0, 0, 0] * maxSize
        self.count = 0
        self.m = filter_capacity

    def length(self):
        # 求数组的长度
        return self.count

    def show(self):
        if self.count <= 0:
            print('null')
        else:
            print(self.li[: self.count])

    def add(self, value, bucket_index):
        if self.count >= self.maxSize:  # 判断是否数组越界
            raise Exception('full')

        # 将新节点增加到最后
        if value[1] == 0:
            self.li[self.count] = [value[0] * self.m + bucket_index, value[2]]

        if value[1] == 1:
            self.li[self.count] = [bucket_index * self.m + value[0], value[2]]

        self._shift_up(self.count)  # 递归构建大堆
        self.count += 1

    def _shift_up(self, index):
        # 往大堆中添加元素，并保证根节点是最大的值:
        # 1.增加新的值到最后一个结点，在add实现； 2.与父节点比较，如果比父节点值大，则交换
        if index > 0:
            parent = (index - 1) // 2  # 找到根节点
            if self.li[index][1] > self.li[parent][1]:  # 交换结点
                self.li[index], self.li[parent] = self.li[parent], self.li[index]
                self._shift_up(parent)  # 继续递归从底往上判断

    def extract(self):
        # 弹出最大堆的根节点，即最大值
        # 1.删除根结点，将最后一个结点作为更结点 ； 2.判断根结点与左右结点的大小，交换左右结点较大的
        if not self.count:
            raise Exception('null')
        value = self.li[0]
        self.count -= 1
        self.li[0] = self.li[self.count]  # 将最后一个值变为第一个
        self._shift_down(0)
        return value

    def _shift_down(self, index):
        # 1.判断是否有左子节点并左大于根，左大于右；2.判断是否有右子节点，右大于根
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index
        # 判断条件
        # 下面2个条件包含了，判断左右结点那个大的情况。如果为3， 4， 5,：第一个判断条件使得largest = 1，再执行第二个条件，则判断其左结点与右结点的大小
        if left < self.length() and self.li[left][1] > self.li[largest][1]:
            largest = left
        if right < self.length() and self.li[right][1] > self.li[largest][1]:
            largest = right

        if largest != index:  # 将 两者交换
            self.li[index], self.li[largest] = self.li[largest], self.li[index]
            self._shift_down(largest)


def rank(target_AF=Topk_Ark_Filter.Topk_Ark_Filter(capacity=1024)):
    for i in range(target_AF.capacity):
        result = sorted(target_AF.buckets[i].bucket, key=(lambda x: x[2]), reverse=True)
        target_AF.buckets[i].bucket = result
    return True


def maxheap_for_topk(target_AF=Topk_Ark_Filter.Topk_Ark_Filter(capacity=1024), number_of_floors=1, k=10):
    result = []
    rank(target_AF)
    m = MaxHeap(maxSize=math.ceil(number_of_floors * target_AF.capacity), filter_capacity=target_AF.capacity)
    for i in range(number_of_floors):
        for j in range(target_AF.capacity):
            if len(target_AF.buckets[j].bucket) > i:
                m.add(value=target_AF.buckets[j].bucket[i], bucket_index=j)

    for num in range(k + int(k / 20)):
        result.append(m.extract())

    return result


def minheap_for_topk(target_AF=Topk_Ark_Filter.Topk_Ark_Filter(capacity=1024), number_of_floors=1, k=10):
    rank(target_AF)
    minheap = MinHeap(maxsize=k)
    for i in range(number_of_floors):
        for j in range(target_AF.capacity):
            if len(target_AF.buckets[j].bucket) >= number_of_floors:
                if target_AF.buckets[j].bucket[i][1] == 0:
                    minheap.heavy_keep(target_AF.buckets[j].bucket[i][0] * target_AF.capacity + j,
                                       target_AF.buckets[j].bucket[i][2])
                if target_AF.buckets[j].bucket[i][1] == 1:
                    minheap.heavy_keep(j * target_AF.capacity + target_AF.buckets[j].bucket[i][0],
                                       target_AF.buckets[j].bucket[i][2])

            if len(target_AF.buckets[j].bucket) < number_of_floors and i < len(target_AF.buckets[j].bucket):
                if target_AF.buckets[j].bucket[i][1] == 0:
                    minheap.heavy_keep(target_AF.buckets[j].bucket[i][0] * target_AF.capacity + j,
                                       target_AF.buckets[j].bucket[i][2])
                if target_AF.buckets[j].bucket[i][1] == 1:
                    minheap.heavy_keep(j * target_AF.capacity + target_AF.buckets[j].bucket[i][0],
                                       target_AF.buckets[j].bucket[i][2])

    return minheap
