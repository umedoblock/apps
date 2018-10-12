# Copyright 2011-2015 梅濁酒(umedoblock)

from pyeijiro import isascii
count = 0
f = open('key.txt')
for l in f.readlines():
  l = l.strip()
  if not isascii(l):
    print(l)
    count += 1
print('count =', count)
