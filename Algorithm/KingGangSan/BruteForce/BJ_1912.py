# 연속합 - 완전탐색, 브루트 포스 서치. Brute Force Search
'''
(시간제한 1초)

(문제 설명)
n개의 정수로 이루어진 임의의 수열이 주어진다. 우리는 이 중 연속된 몇 개의 수를 선택해서 구할 수 있는 합 중 가장 큰 합을 구하려고 한다. 단, 수는 한 개 이상 선택해야 한다.

예를 들어서 10, -4, 3, 1, 5, 6, -35, 12, 21, -1 이라는 수열이 주어졌다고 하자. 여기서 정답은 12+21인 33이 정답이 된다.

(예제 입력1)
10
10 -4 3 1 5 6 -35 12 21 -1

<해설>
앞에서부터 부분합을 구해 가면서, 가장 큰 부분합을 찾는 문제이다.
앞에서부터 구한 부분합보다 지금 보고 있는 index의 요소가 더 크다면, 그 뒤부터는 항상! 현재 index부터의 부분합이 앞에서부터 구한 부분합보다 크다.
'''

# 후보 1
# 이렇게 하면 시간초과가 뜬다.
# n이 최대 100,000이며, for문 2개 + sum을 거치므로 대략 10^18 또는 그 이하(두번째 for문에서는 log일 가능성 있음) --> 1초에 10^8
# 계산하는 컴퓨터와 비교했을 때 문제가 생길 가능성 존재함.
N = int(input())
arr = list(map(int, input().split()))
max_ = -10e9
for window in range(2, N+1):
    for i in range(N-window+1):
        sum_ = sum(arr[i:i+window-1])
        if max_ < sum_:
            max_ = sum_
print(max_)


# 정답
N = int(input())
arr = list(map(int, input().split()))
 
for i in range(1, N):
    arr[i] = max(arr[i], arr[i] + arr[i-1])
    # 현재 index의 요소값과, 현재 index에서부터 이전 모든 부분합을 비교한다.
    # 이 과정은 현재 index부터의 부분합이 이전 모든 index들과의 합과 비교해서 유의미한 값인지를 비교하는 것.
    # arr[i]가 크다면, 해답은 index i부터 시작하는 부분합일 가능성이 존재하며, 그 이전부터 시작하는 부분합이 해답이 될 경우는 없어진다.
    # arr[i]+arr[i-1]이 크다면, index i 부터 시작하는 부분합이 해답이 될 가능성은 없어진다.
    
print(max(arr))
 