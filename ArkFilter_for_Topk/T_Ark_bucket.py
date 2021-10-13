import random


class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = []

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
        index = self.is_exist(item=item, f=1)
        if index != -1:
            self.bucket[index][2] += 1
            return True
        else:
            if not self.is_full():
                self.bucket.append([item, 1, 1])
                return True
        return False

    def R_insert(self, item):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        index = self.is_exist(item=item, f=0)
        if index != -1:
            self.bucket[index][2] += 1
            return True
        else:
            if not self.is_full():
                self.bucket.append([item, 0, 1])
                return True
        return False

    def insert(self, item, f, counts):
        if not self.is_full():
            self.bucket.append([item, abs(f - 1), counts])
            return True
        return False

    def Q_delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        index = self.is_exist(item=item, f=1)
        if index == -1:
            return False

        if self.bucket[index][2] > 1:
            self.bucket[index][2] -= 1
            return True
        else:
            del self.bucket[index]
            return True


    def R_delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        index = self.is_exist(item=item, f=0)
        if index == -1:
            return False

        if self.bucket[index][2] > 1:
            self.bucket[index][2] -= 1
            return True
        else:
            del self.bucket[index]
            return True


    def is_full(self):
        return len(self.bucket) == self.size

    def is_exist(self, item, f):
        for i in range(len(self.bucket)):
            if self.bucket[i][0] == item and self.bucket[i][1] == f:
                return i
        return -1

    def swap(self, item, f, counts):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param item:
        :return:
        """
        index = random.choice(range(len(self.bucket)))  # 从桶的槽中随机选一个
        swapped_item = self.bucket[index]
        self.bucket[index] = [item, abs(f - 1), counts]
        return swapped_item

