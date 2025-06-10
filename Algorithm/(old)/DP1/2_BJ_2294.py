'''

import sys      # sys모듈을 불러온뒤import sys
sys.setrecursionlimit(10000)    # 재귀의 한도를 10000까지 풀어준다.
# 거꾸로 DP를 하려면 어떡하지? 탑다운 방식으로 하려면? --> 재귀함수를 만드는 수밖에 없나.
n, target_value = map(int, input().split())
coins = []
for _ in range(n):
    coins.append(int(input()))
coins.sort()

# 계속 indexError가 났던 이유?
# 처음에 dp를 아래처럼 정의했다.
# dp = [0]*(target_value+1)
# 이렇게 하면 coin의 가장 높은 값 밸류가 k보다 클 경우, index error를 만들어낼 수 있다...
max_index = max(coins[-1], target_value)
dp = [0]*(max_index+1)

# dp를 초기화해줬다 미리.
# print('계산된 친구들 1 : ', end=' ')
for c in coins:
    # print(c, ', ', end=' ')
    dp[c] = 1
# print('')

# print('계산된 친구들 2 : ', end=' ')
for i in range(coins[0]):
    # print(i, ', ', end=' ')
    dp[i] = -1
# print('')

def recurrent(coins, k):
    # print(f'{k}번째 값 구하기 시작 ..')
    global dp

    if dp[k]>0:
        return dp[k]

    else:
        candidates = []
        for coin in coins:
            if k-coin > 0 :
                if dp[k-coin] == -1:
                    # print(f'{k}번째 값 구하는 중 .. {k-coin}? 불가능.')
                    pass
                elif dp[k-coin] == 0:
                    # print(f'{k}번째 값 구하는 중 .. {k-coin}? 아직 계산 안함.')
                    dp[k-coin] = recurrent(coins, k-coin)
                    if dp[k-coin] > 0:
                        candidates.append(dp[k-coin])
                else:
                    # print(f'{k}번째 값 구하는 중 .. {k-coin}? 이미 계산되어 있음.')
                    candidates.append(dp[k-coin])

        if candidates:
            dp[k] = min(candidates) + 1
            # print(f'{k}번째 값은 {dp[k]}였습니다. dp에 저장됨')
            return dp[k]
        else:
            dp[k] = -1
            # print(f'{k}번째 값은 {dp[k]}였습니다. dp에 저장됨')
            return -1
    

print(recurrent(coins, target_value))
# print(dp)
'''



# 위에 거 재귀 깊이 100000으로 만들면 돌아가네요

