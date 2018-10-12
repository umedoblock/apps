# Copyright 2011-2015 梅濁酒(umedoblock)

import collections
import time

# wdict1 make time is 5.256090879440308
# wdict2 make time is 3.7691729068756104

name = 'key.txt'
f = open(name)
lines = f.readlines()
f.close()

words = []
for line in lines:
    line = line.strip()
    ws = line.split('|')
    L = []
    for w in ws:
        L.extend(w.split(' '))
    words.extend(L)

words.sort()

s = time.time()
wdict1 = {}
for word in words:
    if word not in wdict1:    # このif文が何度も実行されて無駄
        wdict1[word] = 0
    wdict1[word] += 1
e = time.time()
t = e - s
print('wdict1 make time is', t)

s = time.time()
wdict2 = collections.defaultdict(int)
for word in words:
    wdict2[word] += 1
e = time.time()
t = e - s
print('wdict2 make time is', t)

print('wdict1 == wdict2 is', wdict1 == wdict2)

'''
s = 'mississippi'
d = collections.defaultdict(int)
for k in s:
    d[k] += 1

L1 = list(d.items())
print(L1)
'''
