"""
시간 제한	메모리 제한	제출	정답	맞힌 사람	정답 비율
2 초	512 MB	169483	65763	40948	36.707%
문제
이 문제는 아주 평범한 배낭에 관한 문제이다.

한 달 후면 국가의 부름을 받게 되는 준서는 여행을 가려고 한다. 세상과의 단절을 슬퍼하며 최대한 즐기기 위한 여행이기 때문에, 가지고 다닐 배낭 또한 최대한 가치 있게 싸려고 한다.

준서가 여행에 필요하다고 생각하는 N개의 물건이 있다. 각 물건은 무게 W와 가치 V를 가지는데, 해당 물건을 배낭에 넣어서 가면 준서가 V만큼 즐길 수 있다. 아직 행군을 해본 적이 없는 준서는 최대 K만큼의 무게만을 넣을 수 있는 배낭만 들고 다닐 수 있다. 준서가 최대한 즐거운 여행을 하기 위해 배낭에 넣을 수 있는 물건들의 가치의 최댓값을 알려주자.

입력
첫 줄에 물품의 수 N(1 ≤ N ≤ 100)과 준서가 버틸 수 있는 무게 K(1 ≤ K ≤ 100,000)가 주어진다. 두 번째 줄부터 N개의 줄에 거쳐 각 물건의 무게 W(1 ≤ W ≤ 100,000)와 해당 물건의 가치 V(0 ≤ V ≤ 1,000)가 주어진다.

입력으로 주어지는 모든 수는 정수이다.

출력
한 줄에 배낭에 넣을 수 있는 물건들의 가치합의 최댓값을 출력한다.
"""
N, K = map(int, input().split())
kv = []
k_min = 0
for _ in range(N):
    k, v = map(int, input().split())
    kv.append([k, v])
    # k의 최솟값 구하는 이유: base_case 위해서. k보다 작은 무게의 가방(dp)에 대해서는 0이 나옴
    if k_min == 0 or k_min > k:
        k_min = k # 3
    
dp = [0] * k_min + [-1] * (K+1) # 어쨌든 K + 1 보다 크면 됨

# print(kv)
def func(K, kv):
    # print(f"BAG K: {K}")
    maxx = 0

    # base case
    if dp[K] != -1:
        return dp[K]
    
    for k, v in kv:
        # print(f"BAG K - {K}, for loop - current k: {k}, v: {v}. dp check = {K-k}")

        # index range 벗어나는 걸 탐색하려 하면 continue
        if K-k < 0:
            continue

        # dp에 등록되어 있다면, dp사용
        if dp[K-k] != -1:
            if maxx < dp[K-k] + v:
                maxx = dp[K-k] + v
                # print(f"BAG K - {K}, k:{k} updated maxx {maxx}, using dp")

        # dp에 등록 안되어 있다면, 재귀호출
        elif dp[K-k] == -1:
            # print(f"BAG K - {K}, k:{k} triggered func")
            r = func(K-k, [x for x in kv if x not in [[k, v]]]) 
            # dp에 업데이트
            dp[K-k] = r
            if maxx < r + v:
                maxx = r + v
                # print(f"BAG K - {K}, k:{k} updated maxx {maxx}, using func")
    return maxx

print(func(K, kv))