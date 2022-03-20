from heapq import heappush, heappop, heapify

l = [5, 8, 12, 3, 2, 5, 6, 7]
h = []
for elmt in l:
    heappush(h, elmt)

print(h)
print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))

a = [45, 5, 2, 124, 78, 23, 20, 8, 1]
heapify(a)
print(a)