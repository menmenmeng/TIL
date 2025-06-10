import time

start_time = time.time()

N = int(input())

dp = [0, 0, 1, 1]

try:
    res = dp[N]

except:
    i = 3
    while True:
        i += 1
        curr_dps = []
        if i%2 == 0 :
            curr_dps.append(dp[i//2])
        if i%3 == 0:
            curr_dps.append(dp[i//3])
        curr_dps.append(dp[i-1])
        
        dp.append(min(curr_dps)+1)
        if i == N:
            res = dp[i]
            break

print(res)

end_time = time.time()

print(end_time - start_time)