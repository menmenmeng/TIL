def next_dp(dp0, dp1, scores):
    next_index = len(dp0)
    dp0.append(max(dp1[next_index-2], dp1[next_index-1]) + scores[0][next_index])
    dp1.append(max(dp0[next_index-2], dp0[next_index-1]) + scores[1][next_index])
    return dp0, dp1

res_list = []
T = int(input())
for _ in range(T):
    n = int(input())
    if n == 1:
        score0 = int(input())
        score1 = int(input())
        res = max(score0, score1)

    elif n == 2:
        scores = []
        scores.append(list(map(int, input().split())))
        scores.append(list(map(int, input().split())))
        res = max(scores[1][0]+scores[0][1], scores[0][0]+scores[1][1])

    else:
        scores = []
        scores.append(list(map(int, input().split())))
        scores.append(list(map(int, input().split())))
        dp0 = [scores[0][0], scores[1][0]+scores[0][1]]
        dp1 = [scores[1][0], scores[0][0]+scores[1][1]]
        while True:
            try:
                dp0, dp1 = next_dp(dp0, dp1, scores)
            except:
                break
        res = max(dp0[-1], dp1[-1])
    res_list.append(res)

for result in res_list:
    print(result)