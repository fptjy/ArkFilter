import D_Ark_Filter
import random
import D_exceptions


def dynamic_increase(target_AF=D_Ark_Filter.Ark_Filter(capacity=1024), increase_size=1):
    """
    DAF scales up by increasing the number of slots in each bucket adaptively.

    Once the space utilization of filter reaching the predefined threshold value, it triggers dynamic_increase.

    :param target_AF: target Ark Filter which needs to scale up.
    :param increase_size: the expanded size of target Ark Filter.
    :return: True.
    """
    for i in range(target_AF.capacity):
        for j in range(increase_size):
            target_AF.buckets[i].bucket.append([-1, 0])
    return True


def daf_insert(data, target_AF=D_Ark_Filter.Ark_Filter(capacity=1024)):
    for i in range(len(data)):
        result = target_AF.insert(data[i])
        if result != "yes":
            dynamic_increase(target_AF=target_AF)
            target_AF.buckets[result[1]].insert(result[0], result[2])
            target_AF.size += 1
    return True


def daf_delete(data, target_AF=D_Ark_Filter.Ark_Filter(capacity=1024)):
    result = True
    for i in range(len(data)):
        if not target_AF.delete(data[i]):
            result = False
    return result


def sort(target_AF=D_Ark_Filter.Ark_Filter(capacity=1024)):
    for i in range(target_AF.capacity):
        count = 0
        for j in range(len(target_AF.buckets[i].bucket)):
            if [-1, 0] in target_AF.buckets[i].bucket:
                del target_AF.buckets[i].bucket[target_AF.buckets[i].bucket.index([-1, 0])]
                count += 1
        for j in range(count):
            target_AF.buckets[i].bucket.append([-1, 0])
    return True


def find_overflow(target_AF=D_Ark_Filter.Ark_Filter(capacity=1024)):
    """
    Find out a bucket with no empty slots
    :param target_AF: target Ark Filter which needs to scale up.
    :return: The index value of the first bucket which has no empty slot. or
            False: all buckets have at least one empty slot.
    """
    for i in range(target_AF.capacity):
        if not target_AF.buckets[i].is_not_full():
            return i
    return -1


def solve_overflow(target_AF=D_Ark_Filter.Ark_Filter(capacity=1024), target_bucket=0):
    """

    """
    bucketsize = len(target_AF.buckets[target_bucket].bucket)

    victim = target_AF.buckets[target_bucket].bucket[-1]
    target_AF.buckets[target_bucket].bucket[-1] = [-1, 0]

    item = target_bucket

    for i in range(50):
        # if i < 50:

        if [-1, 0] in target_AF.buckets[victim[0]].bucket:
            index0 = target_AF.buckets[victim[0]].bucket.index([-1, 0])
        else:
            index0 = bucketsize - 1

        if index0 < (bucketsize - 1):
            target_AF.buckets[victim[0]].bucket[index0] = [item, abs(victim[1] - 1)]
            # return "yes"
            return True
        else:
            index1 = random.choice(range(bucketsize - 1))
            swap_item = target_AF.buckets[victim[0]].bucket[index1]
            target_AF.buckets[victim[0]].bucket[index1] = [item, abs(victim[1] - 1)]
            item = victim[0]
            victim = swap_item

    # return [item, victim[0], abs(victim[1] - 1)]

    #     else:
    #         if [-1, 0] in target_AF.buckets[victim[0]].bucket:
    #             index2 = target_AF.buckets[victim[0]].bucket.index([-1, 0])
    #             target_AF.buckets[victim[0]].bucket[index2] = [item, abs(victim[1] - 1)]
    #             return False
    #         else:
    #             index1 = random.choice(range(bucketsize - 1))
    #             swap_item = target_AF.buckets[victim[0]].bucket[index1]
    #             target_AF.buckets[victim[0]].bucket[index1] = [item, abs(victim[1] - 1)]
    #             item = victim[0]
    #             victim = swap_item
    #
    # return False

    # The number of re-locate operations has reached the threshold
    # we need to put the victim items back into filter when relocation failed
    #

    # sort(target_AF=target_AF)
    #
    if [-1, 0] in target_AF.buckets[victim[0]].bucket:
        target_AF.buckets[victim[0]].bucket[target_AF.buckets[victim[0]].bucket.index([-1, 0])] = [item,
                                                                                                   abs(victim[
                                                                                                           1] - 1)]
        return False
    #
    # if [-1, 0] in target_AF.buckets[item].bucket:
    #     target_AF.buckets[item].bucket[target_AF.buckets[item].bucket.index([-1, 0])] = [victim[0], victim[1]]
    #     return False

    #
    # for xx in range(50):
    #
    #     index1 = random.choice(range(bucketsize))
    #     swap_item = target_AF.buckets[victim[0]].bucket[index1]
    #     target_AF.buckets[victim[0]].bucket[index1] = [item, abs(victim[1] - 1)]
    #     item = victim[0]
    #     victim = swap_item
    #
    #     if [-1, 0] in target_AF.buckets[victim[0]].bucket:
    #         target_AF.buckets[victim[0]].bucket[target_AF.buckets[victim[0]].bucket.index([-1, 0])] = [item,
    #                                                                                                    abs(victim[
    #                                                                                                            1] - 1)]
    #         return False

    return False


def dynamic_decrease(target_AF=D_Ark_Filter.Ark_Filter(capacity=1024)):
    anychange = 1
    if target_AF.size > 0.8 * (len(target_AF.buckets[0].bucket) - 1) * target_AF.capacity:
        # print("target_AF.size:", target_AF.size)
        # print("0.8 * (len(target_AF.buckets[0].bucket) - 1) * target_AF.capacity::",
        #       0.8 * (len(target_AF.buckets[0].bucket) - 1) * target_AF.capacity)
        # print("Did not meet the conditions for dynamic_decrease")
        return False
    #
    if len(target_AF.buckets[0].bucket) == 1:
        find_overflow_result = find_overflow(target_AF=target_AF)
        if find_overflow_result == -1:
            for i in range(target_AF.capacity):
                del target_AF.buckets[i].bucket[-1]
            return True
        else:
            return False

    sort(target_AF=target_AF)
    while (anychange == 1):
        find_overflow_result = find_overflow(target_AF=target_AF)
        if find_overflow_result == -1:
            break
        else:
            # solve_result = solve_overflow(target_AF=target_AF, target_bucket=find_overflow_result)
            # if solve_result != "yes":
            #     target_AF.put_back(solve_result[0], solve_result[1], solve_result[2])
            #     return False
            if not solve_overflow(target_AF=target_AF, target_bucket=find_overflow_result):
                return False

    for j in range(target_AF.capacity):
        del target_AF.buckets[j].bucket[-1]

    return True
