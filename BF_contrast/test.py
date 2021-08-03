from BloomFilter import BloomFilter
from ShiftingBF import ShiftingBF
from Element import Element
from random import randint
from random import seed
from AdaptiveBF import AdaptiveBF

seed(1)
Members, test = [], []
k, max, length  = 4, 32, 3600000
low, up = 1, 100001
for x in range(low,up):
    E = Element(str(x),randint(1,max))
    Members.append(E)
    test.append(E)

for y in range(up,int(2*up)):
    E = Element(str(y),randint(1,max))
    test.append(E)

print("Testing of Adaptive Bloom filter!")
AdapBF =AdaptiveBF(k,length,max)
for e in Members:
    AdapBF.insertion(e.content,e.multiplicity)

correct_ABF = 0
for e in Members:
    if AdapBF.query(e.content) == e.multiplicity:
        correct_ABF += 1
print(correct_ABF/len(Members))

FPR_ABF = 0
for i in range(len(Members),len(test)):
    if AdapBF.query(test[i].content):
        FPR_ABF += 1
print(FPR_ABF)    

print("Testing of Shifting Bloom filter!")
  # testing of Shifting Bloom Filter
ShiftBF = ShiftingBF(k,length,max)
for e in Members:
    ShiftBF.insertion(e.content,e.multiplicity)

correct_SBF = 0
for e in Members:
    if ShiftBF.query(e.content) == e.multiplicity:
        correct_SBF += 1
print(correct_SBF/len(Members))

FPR_SBF = 0
for i in range(len(Members),len(test)):
    if ShiftBF.query(test[i].content):
        FPR_SBF += 1
print(FPR_SBF)