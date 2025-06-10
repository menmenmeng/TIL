import sys

n, k = map(int, sys.stdin.readline().split())
coins = []
for _ in range(n):
    coins.append(int(input()))

coins.sort()
# bottom-up 생각해보자.

dp = [0]
for i in range(1, k+1):
    candidates = []
    for c in coins:
        if i - c < 0:
            break
        if dp[i-c] == -1:
            continue
        candidates.append(dp[i-c])

    if len(candidates) > 0:
        dp.append(min(candidates) + 1)
    else:
        dp.append(-1)

print(dp[k])