from __future__ import absolute_import
import hashlib
from utils import range_fn, running_python_3
from struct import unpack, pack

try:
    import bitarray
except ImportError:
    raise ImportError('pybloom requires bitarray >= 0.3.4')


class Adaptive_BloomFilter(object):
    """description of class"""

    def __init__(self, k, m, max):
        self.m = m  # the length
        self.k = k  # the number of hash functions  # k = 4 and 8
        self.max = max  # the max multiplicity in the set
        self.bitarray = bitarray.bitarray(self.m, endian='little')
        self.bitarray.setall(False)  # the array
        self.make_hashes = make_hashfuncs(self.k + self.max, self.m)

    def query(self, content):
        bitarray = self.bitarray
        hashes_raw = self.make_hashes(content)
        hashes = []
        for h in hashes_raw:
            hashes.append(h)

        for k in hashes[:self.k]:
            if not bitarray[k]:
                return False  # not a member of the set
        for i in range(self.max):
            if not bitarray[hashes[self.k + i]]:
                return i

        return self.max

    def insert(self, content, multiplicity):
        hashes = self.make_hashes(content, self.k + multiplicity)

        if self.max < multiplicity:
            print("out of max")
            return False

        for k in hashes:
            self.bitarray[k] = True

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

    def _make_hashfuncs(key, hash_number=num_slices):
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
                if i >= hash_number:  # 哈希结果的个数取决于这里
                    return

    return _make_hashfuncs
