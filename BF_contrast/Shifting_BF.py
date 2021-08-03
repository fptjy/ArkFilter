from __future__ import absolute_import
import hashlib
from utils import range_fn, running_python_3
from struct import unpack, pack

try:
    import bitarray
except ImportError:
    raise ImportError('pybloom requires bitarray >= 0.3.4')


class Shifting_BloomFilter(object):
    """description of class"""

    def __init__(self, k, m, max):
        self.m = m  # the length
        self.k = k  # the number of hash functions  # k = 4 and 8
        self.max = max  # the max multiplicity in the set
        self.bitarray = bitarray.bitarray(self.m, endian='little')
        self.bitarray.setall(False)  # the array
        self.make_hashes = make_hashfuncs(self.k, self.m - self.max)

    def query(self, content):  # max is the maximum multiplicity in the whole set
        bitarray = self.bitarray
        hashes_raw = self.make_hashes(content)
        hashes = []
        for h in hashes_raw:
            hashes.append(h)

        for k in hashes:
            if not bitarray[k]:
                return False  # not a member of the set

        # result = []
        # for k in hashes:
        #     label = True
        #     for j in range(1, self.max+1):
        #         if bitarray[k+j]:
        #             for k2 in hashes:
        #                 if not bitarray[k2+j]:
        #                     label = False
        #             if label:
        #                 result.append(j+1)
        # return result

        result = []
        h1 = hashes[0]
        for j in range(1, self.max + 1):
            label = True
            if bitarray[h1 + j]:
                for k2 in hashes:
                    if not bitarray[k2 + j]:
                        label = False
                if label:
                    result.append(j + 1)
        return result

    def insert(self, content, multiplicity):
        hashes = self.make_hashes(content)

        if self.max < multiplicity:
            print("out of max")
            return False

        for k in hashes:
            self.bitarray[k] = True  # set the bits for membership as 1s
            try:
                self.bitarray[k + multiplicity - 1] = True  # set the bits for multiplicity
            except:  # may not success
                pass

            # self.bitarray[k + multiplicity - 1] = True  # set the bits for multiplicity

        return True


def make_hashfuncs(num_slices, num_bits):
    if num_bits >= (1 << 31):
        fmt_code, chunk_size = 'Q', 8
    elif num_bits >= (1 << 15):
        fmt_code, chunk_size = 'I', 4
    else:
        fmt_code, chunk_size = 'H', 2

    hashfn = hashlib.md5

    fmt = fmt_code * (hashfn().digest_size // chunk_size)
    num_salts, extra = divmod(num_slices, len(fmt))

    if extra:
        num_salts += 1
    salts = tuple(hashfn(hashfn(pack('I', i)).digest()) for i in range_fn(num_salts))

    def _make_hashfuncs(key):
        if running_python_3:
            if isinstance(key, str):
                key = key.encode('utf-8')
            else:
                key = str(key).encode('utf-8')
        else:
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            else:
                key = str(key)
        i = 0
        for salt in salts:
            h = salt.copy()
            h.update(key)
            for uint in unpack(fmt, h.digest()):
                yield uint % num_bits
                i += 1
                if i >= num_slices:  # 哈希结果的个数取决于这里
                    return

    return _make_hashfuncs
