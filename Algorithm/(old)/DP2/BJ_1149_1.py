N = int(input())
costs = []
for _ in range(N):
    costs.append(list(map(int, input().split())))
    # index : 0 - R, 1 - G, 2 - B

dp = [[('X', k) for k in costs[0]]]

for i in range(1, N):
    dpR = min(dp[i-1][1], dp[i-1][2]) + costs[i]
    dpG = min(dp[i-1][0], dp[i-1][2]) + costs[i]
    dpB = min(dp[i-1][0], dp[i-1][1]) + costs[i]
