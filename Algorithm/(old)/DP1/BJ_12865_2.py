import sys

N, K = map(int, sys.stdin.readline().split())
objects = []
for _ in range(N):
    w, v = map(int, sys.stdin.readline().split())
    objects.append((w, v))

objects.sort(key=lambda x:x[0])

dp = [0]

for i in range(1, K+1):
    candidates = [0]
    for weight, value in objects:
        if i - weight < 0:
            break
        candidates.append(dp[i-weight] + value)
    dp.append(max(candidates))
    
print(dp[K])