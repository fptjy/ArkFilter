"""
    Hash utilities for Ark filters to generate fingerprints.

Generate FNV64 hash based on http://isthe.com/chongo/tech/comp/fnv/
"""
# import mmh3

# def hash_code(data):
#     """Generate hash code using builtin hash() function.
#
#         :param data: Data to generate hash code for
#         """
#     fingerprint = mmh3.hash(data, signed=False)
#     return fingerprint


def hash_code(data):
    """Generate hash code using builtin hash() function.

    :param data: Data to generate hash code for
    """
    # h = 0
    # for c in data:
    #     h = (ord(c) + (31 * h)) % MAX_32_INT
    # return h
    return abs(hash(data))

