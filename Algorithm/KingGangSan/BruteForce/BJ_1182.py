'''
N개의 정수로 이루어진 수열이 있을 때, 크기가 양수인 부분수열 중에서 그 수열의 원소를 다 더한 값이 S가 되는 경우의 수를 구하는 프로그램을 작성하시오.

첫째 줄에 정수의 개수를 나타내는 N과 정수 S가 주어진다. (1 ≤ N ≤ 20, |S| ≤ 1,000,000) 둘째 줄에 N개의 정수가 빈 칸을 사이에 두고 주어진다. 주어지는 정수의 절댓값은 100,000을 넘지 않는다.



<문제오류>...
연속된 부분 수열이 아니어도 된다.

combinations를 활용하는 것이 맞나?
'''

## 부분합을 구한 뒤 for문 두 개 사용하면 풀 수 있을 듯?
# n, s = list(map(int, input().split()))
# if n == 1:
#     seq = int(input())
# else:
#     seq = list(map(int, input().split()))

# cum_seq = [0]
# summ = 0

# try:
#     for elem in seq:
#         summ += elem
#         cum_seq.append(summ)

#     res = 0
#     for i in range(n):
#         for j in range(i+1, n+1):
#             sep = cum_seq[j] - cum_seq[i]
#             if sep == s : 
#                 res += 1
#     print(res)

# except:
#     if seq == s:
#         print(1)
#     else:
#         print(0)

from itertools import combinations


n, s = list(map(int, input().split()))
seq = list(map(int, input().split()))

res = 0
for i in range(1, n+1):
    combs = list(combinations(seq, i))

    for comb in combs:
        summ = sum(comb)
        if summ == s:
            res += 1

print(res)
