def subtract_ArkFilter_with_merge(AF_A, AF_B):
    """
    :param AF_A:
    :param AF_B:
    :return: AF_A - AF_B
    """

    for i in range(AF_A.capacity):
        for j in range(len(AF_A.buckets[i].bucket)):
            item = AF_A.buckets[i].bucket[j]
            if AF_B.contains_fingerprint(item, i):
                AF_A.size -= 1
                AF_A.buckets[i].bucket[j] = -1


def subtract_ArkFilter(AF_A, AF_B):
    """
    :param AF_A:
    :param AF_B:
    :return: AF_A - AF_B
    """

    for i in range(AF_A.capacity):
        for j in range(len(AF_A.buckets[i].bucket)):
            item = AF_A.buckets[i].bucket[j][0]
            label = AF_A.buckets[i].bucket[j][1]
            if AF_B.contains_fingerprint(item, label, i):
                AF_A.size -= 1
                AF_A.buckets[i].bucket[j] = [-1, 0]


def subtract_CuckooFilter(CF_A, CF_B):
    for i in range(CF_A.capacity):
        for j in range(len(CF_A.buckets[i].bucket)):
            fingerprint = CF_A.buckets[i].bucket[j]
            if CF_B.contains_fingerprint(fingerprint, i):
                CF_A.size -= 1
                CF_A.buckets[i].bucket[j] = -1


def intersection_ArkFilter_with_merge(AF_A, AF_B):
    """
    :param AF_A:
    :param AF_B:
    :return: AF_A v AF_B
    """

    for i in range(AF_A.capacity):
        for j in range(len(AF_A.buckets[i].bucket)):
            item = AF_A.buckets[i].bucket[j]
            if not AF_B.contains_fingerprint(item, i):
                AF_A.size -= 1
                AF_A.buckets[i].bucket[j] = -1


def intersection_ArkFilter(AF_A, AF_B):
    """
    :param AF_A:
    :param AF_B:
    :return: AF_A v AF_B
    """

    for i in range(AF_A.capacity):
        for j in range(len(AF_A.buckets[i].bucket)):
            item = AF_A.buckets[i].bucket[j][0]
            label = AF_A.buckets[i].bucket[j][1]
            if not AF_B.contains_fingerprint(item, label, i):
                AF_A.size -= 1
                AF_A.buckets[i].bucket[j] = [-1, 0]


def intersection_CuckooFilter(CF_A, CF_B):
    for i in range(CF_A.capacity):
        for j in range(len(CF_A.buckets[i].bucket)):
            fingerprint = CF_A.buckets[i].bucket[j]
            if not CF_B.contains_fingerprint(fingerprint, i):
                CF_A.size -= 1
                CF_A.buckets[i].bucket[j] = -1
