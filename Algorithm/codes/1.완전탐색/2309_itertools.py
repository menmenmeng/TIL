import itertools

heights = []
for _ in range(9):
    h = int(input())
    heights.append(h)

combination = list(itertools.combinations(heights, 7))

for comb in combination:
    if sum(comb) == 100:
        comb = list(comb)
        comb.sort()
        for i in comb:
            print(i, end='\n')
        break