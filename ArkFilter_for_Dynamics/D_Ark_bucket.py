import random


class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = [[-1, 0] for i in range(size)]

    def __repr__(self):
        return '<Bucket: ' + str(self.bucket) + '>'

    def __contains__(self, item):
        return item in self.bucket

    def __len__(self):
        return len(self.bucket)

    def Q_insert(self, item):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if self.is_not_full():
            self.bucket[self.bucket.index([-1, 0])] = [item, 1]
            return True
        return False

    def R_insert(self, item):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if self.is_not_full():
            self.bucket[self.bucket.index([-1, 0])] = [item, 0]
            return True
        return False

    def insert(self, item, f):
        if self.is_not_full():
            self.bucket[self.bucket.index([-1, 0])] = [item, abs(f - 1)]
            return True
        return False

    def Q_delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        try:
            self.bucket[self.bucket.index([item, 1])] = [-1, 0]
            return True
        except ValueError:
            return False

    def R_delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        try:
            self.bucket[self.bucket.index([item, 0])] = [-1, 0]
            return True
        except ValueError:
            return False

    def is_not_full(self):
        return [-1, 0] in self.bucket

    def swap(self, item, f):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param item:
        :return:
        """
        index = random.choice(range(len(self.bucket)))  # 从桶的槽中随机选一个
        swapped_item = self.bucket[index]
        self.bucket[index] = [item, abs(f - 1)]
        return swapped_item
