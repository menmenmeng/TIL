N = int(input())

# bottom-up방식 구현
# bottom-up이 더 빠르다... ㅎ 왜지.

dp = [0, 0, 1, 1]

if N in (1, 2, 3):
    print(dp[N])

else:
    for i in range(4, N+1):
        l = []
        if i % 3 == 0:
            l.append(dp[i//3])
        if i % 2 == 0:
            l.append(dp[i//2])
        l.append(dp[i-1])

        dp.append(min(l)+1)

    print(dp[N])