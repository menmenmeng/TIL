# N = int(input())

# f_list = [-1] * 90
# g_list = [-1] * 90

# # 1로 끝나는 n자리 이친수의 개수를 구하는 함수
# def f(n):
#     if n == 1:
#         return 1
    
#     else:
#         if g_list[n-1] >= 0:
#             gg = g_list[n-1]

#         else:
#             gg = g(n-1)
        
#         return gg

# # 0으로 끝나는 n자리 이친수의 개수를 구하는 함수
# def g(n):
#     if n == 1:
#         return 0
    
#     elif n == 2:
#         return 1
    
#     else:
#         if f_list[n-1] >= 0:
#             ff = f_list[n-1]
#         else:
#             ff = f(n-1)

#         if g_list[n-1] >= 0:
#             gg = g_list[n-1]
#         else:
#             gg = g(n-1)

#         return ff + gg
    
# print(g(N) + f(N))


# 위의 풀이 시간초과 이유 : g(n) = f(n-1) + g(n-1) // f(n) = g(n-1) 이면,
# g(n) = f(n-1) + g(n-1) -> g(n-2) + g(n-1)로 놓으면 됨. 즉 g만 계산하면 f를 계산할 필요는 없다
# 지금 확인했는데 중요한게 메모이제이션을 안썼네......

N = int(input())
g_list = [-1] * 91

def f(n):
    if n == 1:
        return 1
    
    else:
        return g(n-1)


def g(n):
    if n == 1:
        return 0
    
    elif n == 2:
        return 1
    
    else:
        if g_list[n-1] >= 0:
            gn_1 = g_list[n-1]
        else:
            g_list[n-1] = g(n-1)
            gn_1 = g_list[n-1]
        
        if g_list[n-2] >= 0:
            gn_2 = g_list[n-2]
        else:
            g_list[n-2] = g(n-2)
            gn_2 = g_list[n-2]
        
        return gn_1 + gn_2
    
print(f(N) + g(N))