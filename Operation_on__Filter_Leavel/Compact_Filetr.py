import random


def compact_ArkFilter(AF_A, AF_B):
    for i in range(AF_B.capacity):
        for j in range(len(AF_B.buckets[i].bucket)):
            insert_AF(AF_A=AF_A, i=i, item=AF_B.buckets[i].bucket[j][0], label=AF_B.buckets[i].bucket[j][1])


def insert_AF(AF_A, i, item, label):
    if AF_A.buckets[i].insert(item, abs(label - 1)) or AF_A.buckets[item].insert(i, label):
        AF_A.size += 1
        return True

    # SWAP = AF_A.buckets[i].swap(item, abs(label - 1)) #反而慢了
    # C = SWAP[0]
    # f = SWAP[1]
    # T = i

    T = random.choice([i, item])
    slot_index = random.choice(range(len(AF_A.buckets[T].bucket)))
    C = AF_A.buckets[T].bucket[slot_index][0]
    f = AF_A.buckets[T].bucket[slot_index][1]

    if T == i:
        AF_A.buckets[T].bucket[slot_index][0] = item
        AF_A.buckets[T].bucket[slot_index][1] = label
    if T == item:
        AF_A.buckets[T].bucket[slot_index][0] = i
        AF_A.buckets[T].bucket[slot_index][1] = abs(label - 1)

    for _ in range(AF_A.max_displacements):
        if AF_A.buckets[C].insert(T, f):
            AF_A.size += 1
            return True
        _swap_ = AF_A.buckets[C].swap(T, f)
        T = C
        C = _swap_[0]
        f = _swap_[1]
    return False


def compact_CuckooFilter(CF_A, CF_B):
    for i in range(CF_B.capacity):
        for j in range(len(CF_B.buckets[i].bucket)):
            insert_CF(CF_A=CF_A, i=i, fingerprint=CF_B.buckets[i].bucket[j])


def insert_CF(CF_A, i, fingerprint):
    candidate_bucket = CF_A._get_alternate_index(i, fingerprint)

    if CF_A.buckets[i].insert(fingerprint) \
            or CF_A.buckets[candidate_bucket].insert(fingerprint):
        CF_A.size += 1
        return True

    eviction_index = random.choice([i, candidate_bucket])
    for _ in range(CF_A.max_displacements):
        f = CF_A.buckets[eviction_index].swap(fingerprint)
        eviction_index = CF_A._get_alternate_index(eviction_index, f)
        if CF_A.buckets[eviction_index].insert(f):
            CF_A.size += 1
            return True
        fingerprint = f
    return False


def compact_ArkFilter_with_merge(AF_A, AF_B):
    for i in range(AF_B.capacity):
        for j in range(len(AF_B.buckets[i].bucket)):
            insert_AF_withmerge(AF_A=AF_A, i=i, item=AF_B.buckets[i].bucket[j])


def insert_AF_withmerge(AF_A, i, item):
    if AF_A.buckets[i].insert2(item) or AF_A.buckets[int(item[:-1])].insert2(str(i) + str(abs(int(item[-1]) - 1))):
        AF_A.size += 1
        return True

    j = int(item[:-1])
    T = random.choice([i, j])

    if T == i:
        f = AF_A.buckets[T].swap2(item)

    if T == j:
        f = AF_A.buckets[T].swap2(str(i) + str(abs(int(item[-1]) - 1)))

    for _ in range(AF_A.max_displacements):
        if AF_A.buckets[int(f[:-1])].insert(str(T) + f[-1]):
            AF_A.size += 1
            return True
        else:
            _swap_ = AF_A.buckets[int(f[:-1])].swap(str(T) + f[-1])
            T = int(f[:-1])
            f = _swap_
    return False
