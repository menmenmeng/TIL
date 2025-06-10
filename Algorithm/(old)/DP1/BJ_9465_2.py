import sys

T = int(input())

# 각 테스트 케이스에 대해.
res_test_cases = []
for _ in range(T):

    # 테스트 케이스의 가로 스티커 개수
    N = int(input())

    # 테스트 케이스의 2개 행
    stickers = []
    for _ in range(2):
        stickers.append(list(map(int, sys.stdin.readline().split())))

    # 2차원 dp
    dp = [[-1] * N,[-1] * N]

    for n in range(N):
        if n == 0:
            dp[0][n] = stickers[0][n]
            dp[1][n] = stickers[1][n]

        elif n == 1:
            dp[0][n] = dp[1][n-1] + stickers[0][n]
            dp[1][n] = dp[0][n-1] + stickers[1][n]

        else:
            dp[0][n] = max(dp[0][n-2], dp[1][n-2], dp[1][n-1]) + stickers[0][n]
            dp[1][n] = max(dp[0][n-2], dp[1][n-2], dp[0][n-1]) + stickers[1][n]
            
    res_test_cases.append(max(dp[0][N-1], dp[1][N-1]))

for res in res_test_cases:
    print(res)