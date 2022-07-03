# 입력 : 5 8 3 \n 2 4 5 4 6
# 출력 : 46
n, m, k = map(int, input().split())
nums = list(map(int, input().split()))
nums.sort()

big_num = 0
k_num = 0
for _ in range(m):
    if k_num != k:
        k_num += 1
        big_num += nums[-1]

    elif k_num == k:
        k_num = 0
        big_num += nums[-2]

print(big_num)