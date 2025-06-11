"""
문제
정수 X에 사용할 수 있는 연산은 다음과 같이 세 가지 이다.

X가 3으로 나누어 떨어지면, 3으로 나눈다.
X가 2로 나누어 떨어지면, 2로 나눈다.
1을 뺀다.
정수 N이 주어졌을 때, 위와 같은 연산 세 개를 적절히 사용해서 1을 만들려고 한다. 연산을 사용하는 횟수의 최솟값을 출력하시오.

입력
첫째 줄에 1보다 크거나 같고, 106보다 작거나 같은 정수 N이 주어진다.

출력
첫째 줄에 연산을 하는 횟수의 최솟값을 출력한다.
"""
X = int(input())

## DP용 배열은 dictionary를 쓰자. list 쓸 경우, index = -1에 대한 보상로직이 있을 경우를 추가 고민해야 함...

# 엄청 빨리 끝나는 모범답안. Top-down 방식으로 했다. 그런데 나눠져서 나머지가 얼마냐를 굳이 따지지 않음.
# counts = [-1] * (X+1)
# counts[1] = 0
# 위처럼 하면 RecursionError가 뜬다. 초기값을 1, 2, 3 모두 지정해줄 수 있다. 
counts = [-1, 0, 1, 1] + [-1] * X
# counts = {1:0, 2:1, 3:1}
def func(X):
    if counts[X] != -1:
        return counts[X]
    else:
        counts[X] = 1 + min(func(X//3) + X%3, func(X//2) + X%2) # 나머지가 있으면 나머지는 그냥 X+1 연산을 한다고 친다.
        return counts[X]

print(func(X))



# # Bottom-up 방식
# counts = [-1, 0] + [-1] * (X-1)

# idx = 2
# while idx <= X:
#     l = []
#     if idx % 3 == 0:
#         l.append(counts[idx//3] + 1)
#     if idx % 2 == 0:
#         l.append(counts[idx//2] + 1)
#     l.append(counts[idx-1] + 1)

#     counts[idx] = min(l)
#     idx += 1

# print(counts[X])


# # Top-down 방식으로 구현했는데, recursion Error 발생했음. 기본적으로 Top-down 으로 하면 recursionError 발생하는듯 이 문제는..
# counts = [-1] * (X+1)
# counts[1] = 0
# def func(X):
#     if X == 1:
#         return counts[X] # 1에서 1로 만드는 건 횟수 0번.
#     elif counts[X] != -1: # 계산이 되었다면?
#         return counts[X]
#     else:
#         res = []
#         if X % 3 == 0:
#             num = func(X//3)
#             res.append(num)
#         if X % 2 == 0:
#             num = func(X//2)
#             res.append(num) # 1
#         num = func(X-1)
#         res.append(num) # 1
#         fin_res = min(res) + 1
#         counts[X] = fin_res
#         return fin_res
# print(func(X))