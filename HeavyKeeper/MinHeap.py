class MinHeap(object):
    """
    Achieve a minimum heap by Array
    """

    def __init__(self, maxsize=None):
        self.maxsize = maxsize
        self._elements = [["id", 0] for i in range(self.maxsize)]
        self._count = 0

    def __len__(self):
        return self._count

    def add(self, key, value):
        """
        Add an element to heap while keeping the attribute of heap unchanged.
        :param value: the value added to the heap
        :return: None
        """
        if self._count >= self.maxsize:
            raise Exception("The heap is full!")
        self._elements[self._count][0] = key
        self._elements[self._count][1] = value
        self._count += 1
        self._siftup(self._count - 1)

    def _siftup(self, index):
        """
        To keep the the attribute of heap unchanged while adding a new value.
        :param index: the index of value you want to swap
        :return: None
        """
        if index > 0:
            parent = int((index - 1) / 2)
            if self._elements[parent][1] > self._elements[index][1]:
                self._elements[parent], self._elements[index] = self._elements[index], self._elements[parent]
                self._siftup(parent)

    def extract(self):
        """
        pop and return the value of root
        :return: the value of root
        """
        if self._count <= 0:
            raise Exception('The heap is empty!')

        value = self._elements[0]
        self._count -= 1
        self._elements[0] = self._elements[self._count]
        self._siftdown(0)
        return value

    def _siftdown(self, index):
        """
        to keep the attribute of heap unchanged while pop out the root node.
        :param index: the index of value you want to swap
        :return: None
        """
        if index < self._count:
            left = 2 * index + 1
            right = 2 * index + 2
            if left < self._count and right < self._count \
                    and self._elements[left][1] <= self._elements[right][1] \
                    and self._elements[left][1] <= self._elements[index][1]:
                self._elements[left], self._elements[index] = self._elements[index], self._elements[left]
                self._siftdown(left)

            elif left < self._count and right < self._count \
                    and self._elements[left][1] >= self._elements[right][1] \
                    and self._elements[right][1] <= self._elements[index][1]:
                self._elements[right], self._elements[index] = self._elements[index], self._elements[right]
                self._siftdown(left)

            if left < self._count and right > self._count \
                    and self._elements[left][1] <= self._elements[index][1]:
                self._elements[left], self._elements[index] = self._elements[index], self._elements[left]
                self._siftdown(left)

    def heavy_keep(self, key, value):
        """
        Add no more than maxsize elements to heap while keeping the attribute of heap unchanged.
        and keep the big elements
        :param value: the value added to the heap
        :return: None
        """
        if self._count < self.maxsize:
            self._elements[self._count][0] = key
            self._elements[self._count][1] = value
            self._count += 1
            self._siftup(self._count - 1)
            return True

        if self._count >= self.maxsize:
            if self._elements[0][1] < value:
                self._elements[0][0] = key
                self._elements[0][1] = value
                self._siftdown(0)
                return True
