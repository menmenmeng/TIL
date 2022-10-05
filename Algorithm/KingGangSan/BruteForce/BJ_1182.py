'''
N개의 정수로 이루어진 수열이 있을 때, 크기가 양수인 부분수열 중에서 그 수열의 원소를 다 더한 값이 S가 되는 경우의 수를 구하는 프로그램을 작성하시오.

첫째 줄에 정수의 개수를 나타내는 N과 정수 S가 주어진다. (1 ≤ N ≤ 20, |S| ≤ 1,000,000) 둘째 줄에 N개의 정수가 빈 칸을 사이에 두고 주어진다. 주어지는 정수의 절댓값은 100,000을 넘지 않는다.



<문제오류>...
연속된 부분 수열이 아니어도 된다.

combinations를 활용하는 것이 맞나?
'''

## 부분합을 구한 뒤 for문 두 개 사용하면 풀 수 있을 듯?
## 이거 안되는 이유 : 연속된 부분 수열이 아니어도 되기 때문..! 후우.
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


# itertools 의 combinations를 활용한 방법
'''
from itertools import combinations


n, s = list(map(int, input().split())) # list로 안 묶어도 됨.
seq = list(map(int, input().split()))

res = 0
for i in range(1, n+1):
    combs = list(combinations(seq, i)) # list로 안 묶어도 된다. combinations 객체는 그 자체로 이미 iterator니까.

    for comb in combs:
        summ = sum(comb)
        if summ == s:
            res += 1

print(res)
'''


# 재귀함수를 활용하는 방법
n, s = map(int, input().split())
seq = list(map(int, input().split()))

cnt = 0
def sub_sum(idx, sum_former):
    # global cnt # global 변수를 사용하지 않으면 조금 어려운 듯. 왜냐? 재귀함수 갈래가 계속해서 2개로 나뉘어지는데, 그 모든 재귀함수들의 결과값을 하나의 값에 담아야 함.
    # 아니면, 전부를 더하는 게 아니라. return되는 값이 이때까지의. 모든 재귀함수들의 cnt를 더한 값. 이라고 할 수도 있을 듯.

    tmp_cnt = 0
    if idx==n-1:
        if sum_former+seq[idx] == s:
            tmp_cnt += 1


        return tmp_cnt

    else:
        idx2 = idx + 1
        subSum = sum_former + seq[idx]
        if subSum == s:
            return sub_sum(idx2, subSum) + sub_sum(idx2, sum_former) + 1
        else:
            return sub_sum(idx2, subSum) + sub_sum(idx2, sum_former)

print(sub_sum(0, 0))

# 훨씬 빠르고 메모리도 덜 사용한다. 이유가 뭘까?? 적은 개수의 수열을 사용해서?