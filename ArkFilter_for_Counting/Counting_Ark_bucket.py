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

    def Q_insert(self, item, multiplicity):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if not self.is_full():
            self.bucket.append([item, 1, multiplicity])
            return True
        return False

    def R_insert(self, item, multiplicity):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if not self.is_full():
            self.bucket.append([item, 0, multiplicity])
            return True
        return False

    def insert(self, item, f, frequency):
        if not self.is_full():
            self.bucket.append([item, abs(f - 1), frequency])
            return True
        return False

    def is_full(self):
        return len(self.bucket) == self.size

    def swap(self, item, f, frequency):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param item:
        :return:
        """
        index = random.choice(range(len(self.bucket)))  # 从桶的槽中随机选一个
        swapped_item = self.bucket[index]
        self.bucket[index] = [item, abs(f - 1), frequency]
        return swapped_item
