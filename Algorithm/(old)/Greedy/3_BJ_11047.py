# 쉬운 거 같네요

N, K = map(int, input().split())
values = []
for _ in range(N):
    values.append(int(input()))

count = 0
for i in range(N-1, -1, -1):
    count += K//values[i]
    K %= values[i]
    if K==0:
        break

print(count)
