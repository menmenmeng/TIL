# 입력 : a1
# 출력 : 2
col, row = list(input())
col = ord(col) # a : 97, h: 104, row : 1 2 3 4 5 6 7 8
row = int(row)

direction = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

new_place = []
for x, y in direction:
    new_place.append((col+x, row+y))

new_place2 = list(filter(lambda x: (97<=x[0]<=104 and 1<=x[1]<=8), new_place))
print(len(new_place2))