import sys

sys.setrecursionlimit(10**9)

N = int(input())

nums = [-1] * (N+1) # DP memoization

def f(n):
    if n == 1:
        return 0
    elif nums[n] != -1:
        return nums[n]
    else:
        l = [f(n-1)]
        if n % 3 == 0:
            l.append(f(n//3))
        if n % 2 == 0:
            l.append(f(n//2))

    nums[n] = min(l) + 1
    return nums[n]
    
print(f(N))