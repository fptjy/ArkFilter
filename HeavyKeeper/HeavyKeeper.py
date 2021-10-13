''' This module contains the class necessary to implement HeavyKeeperSketch
@author: Pengtao Fu
@Date: 2021/09/12
'''

import numpy as np
import mmh3


class HeavyKeeperSketch(object):
    ''' Class for a HeavyKeeperSketch data structure
        '''

    def __init__(self, width, depth, seeds, finger_size, base=1.08):
        ''' Method to initialize the data structure
        @param width int: Width of the table
        @param depth int: Depth of the table (num of hash func)
        @param seeds list: Random seed list
        '''
        self.width = width
        self.depth = depth
        self.table = [[[0, 0] for i in range(width)] for j in range(depth)]  # Create empty table
        self.seed = seeds  # np.random.randint(w, size = d) // create some seeds
        self.finger_size = finger_size
        self.base = base

    def Generate_fingerprint(self, data):
        """Generate fingerprint using builtin hash() function.

        :param data: Data to generate fingerprint for
        """
        return abs(hash(data)) % self.finger_size

    def insert(self, key):
        ''' Method to add a key to the HeavyKeeper
        @param key str: A string to add to the HeavyKeeper
        '''
        fp = self.Generate_fingerprint(key)
        for i in range(0, self.depth):
            index = mmh3.hash(key, self.seed[i]) % self.width

            if self.table[i][index][1] == 0:
                self.table[i][index][0] = fp
                self.table[i][index][1] = 1

            elif self.table[i][index][0] == fp and self.table[i][index][1] > 0:
                self.table[i][index][1] += 1

            elif self.table[i][index][0] != fp and self.table[i][index][1] > 0:
                if np.random.uniform(0, 1) <= (self.base ** (-self.table[i][index][1])):
                    self.table[i][index][1] -= 1
                    if self.table[i][index][1] == 0:
                        self.table[i][index][0] = fp
                        self.table[i][index][1] = 1

    def query(self, key):
        ''' Method to query a key weather in the HeavyKeeper
        @param key str: A string to query
        '''
        result = 0
        fp = self.Generate_fingerprint(key)
        for i in range(0, self.depth):
            index = mmh3.hash(key, self.seed[i]) % self.width
            if self.table[i][index][0] == fp and self.table[i][index][1] > result:
                result = self.table[i][index][1]

        return result

