"""
문제
자연수 A를 B번 곱한 수를 알고 싶다. 단 구하려는 수가 매우 커질 수 있으므로 이를 C로 나눈 나머지를 구하는 프로그램을 작성하시오.

입력
첫째 줄에 A, B, C가 빈 칸을 사이에 두고 순서대로 주어진다. A, B, C는 모두 2,147,483,647 이하의 자연수이다.

출력
첫째 줄에 A를 B번 곱한 수를 C로 나눈 나머지를 출력한다.
"""

# 지수법칙과 나머지분배법칙을 알아야 하는 거였다. 나머지 관련된 문제가 나왔을 경우, 나머지분배법칙이 큰 도움이 될 수 있음.

A, B, C = map(int, input().split())

def myfunc(A, B, C):
    if B == 1:
        return A % C
    elif B%2==0:
        return (myfunc(A, B//2, C) ** 2) % C
    else:
        return (myfunc(A, B-1, C) * (A % C)) % C
print(myfunc(A, B, C))

# # 시간 초과
# b = 1
# r = A % C
# remains = [r]
# while b < B:
#     # print(r)
#     r = (r * A) % C
#     b += 1
#     if r in remains: # 반복되었다.
#         # print("success")
#         r = remains[B % len(remains)]
#         break
#     remains.append(r)
# print(r)

# # 시간 초과 (0.5초)
# b = 1
# r = A % C
# while b < B:
#     r = (r * A) % C # 무조건 C 보다는 작다.
#     b += 1
# print(r)


# # RecursionError
# def myfunc(A, B, C):
#     if B == 1:
#         return A%C
#     else:
#         (myfunc(A, B-1, C) * A) % C
# if __name__=="__main__":
#     print(myfunc(A, B, C))
