N = int(input())

cnts_rem = {1:1, 2:3, 3:5}
x = 1
while x <= N:
    if x in cnts_rem:
        x += 1
        continue
    cnts_rem[x] = (2*cnts_rem[x-2] + cnts_rem[x-1])%10007
    x += 1

print(cnts_rem[N])