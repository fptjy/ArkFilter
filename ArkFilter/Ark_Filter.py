"""
Ark Filter
"""

import random

import Ark_bucket
import exceptions
import Ark_hashutils


class Ark_Filter(object):
    """
    Ark Filter class.

    Implements insert, delete and contains operations for the filter.
    """

    def __init__(self, capacity, bucket_size=4,
                 max_displacements=500):
        """
        Initialize Ark Filter object.

        :param capacity: Size of the Cuckoo Filter
        :param bucket_size: Number of entries in a bucket
        :param fingerprint_size: Fingerprint size in bytes
        :param max_displacements: Maximum number of evictions before filter is
        considered full
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.max_displacements = max_displacements
        self.buckets = [Ark_bucket.Bucket(size=bucket_size)
                        for _ in range(self.capacity)]
        self.size = 0

    def __repr__(self):        # 重写__repr__()，定义打印class的信息
        return '<ArkFilter: capacity=' + str(self.capacity) + \
               ', size=' + str(self.size) + ' byte(s)>'

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return self.contains(item)

    def _get_fingerprint(self, item):
        finger = Ark_hashutils.hash_code(item) % (self.capacity * (self.capacity - 1))
        return finger

    def _get_R_index(self, fingerprint):
        R_index = fingerprint % self.capacity
        return R_index

    def _get_Q_index(self, fingerprint):
        Q_index = fingerprint // self.capacity
        return Q_index

    def insert(self, item):
        """
        Insert an item into the filter.

        :param item: Item to be inserted.
        :return: True if insert is successful; ArkFilterFullException if
        filter is full.
        """
        fingerprint = self._get_fingerprint(item)
        i = self._get_R_index(fingerprint)
        j = self._get_Q_index(fingerprint)

        if self.buckets[i].R_insert(j) \
                or self.buckets[j].Q_insert(i):
            self.size += 1
            return True

        T = random.choice([i, j])
        slot_index = random.choice(range(len(self.buckets[T].bucket)))
        C = self.buckets[T].bucket[slot_index][0]
        f = self.buckets[T].bucket[slot_index][1]

        if T == i:
            self.buckets[T].bucket[slot_index][0] = j
            self.buckets[T].bucket[slot_index][1] = 0
        if T == j:
            self.buckets[T].bucket[slot_index][0] = i
            self.buckets[T].bucket[slot_index][1] = 1

        for _ in range(self.max_displacements):
            if self.buckets[C].insert(T, f):
                self.size += 1
                return True
            else:
                _swap_ = self.buckets[C].swap(T, f)
                T = C
                C = _swap_[0]
                f = _swap_[1]
        # Filter is full
        return self.size

        # raise exceptions.ArkFilterFullException('Insert operation failed. '
        #                                         'Filter is full.')


    def contains(self, item):
        """
        Check if the filter contains the item.

        :param item: Item to check its presence in the filter.
        :return: True, if item is in the filter; False, otherwise.
        """
        fingerprint = self._get_fingerprint(item)
        i = self._get_R_index(fingerprint)
        j = self._get_Q_index(fingerprint)

        return [j, 0] in self.buckets[i] or [i, 1] in self.buckets[j]


    def delete(self, item):
        """
        Delete an item from the filter.

        To delete an item safely, it must have been previously inserted.
        Otherwise, deleting a non-inserted item might unintentionally remove
        a real, different item that happens to share the same fingerprint.

        :param item: Item to delete from the filter.
        :return: True, if item is found and deleted; False, otherwise.
        """
        fingerprint = self._get_fingerprint(item)
        i = self._get_R_index(fingerprint)
        j = self._get_Q_index(fingerprint)

        if self.buckets[i].R_delete(j) \
                or self.buckets[j].Q_delete(i):
            self.size -= 1
            return True
        return False

