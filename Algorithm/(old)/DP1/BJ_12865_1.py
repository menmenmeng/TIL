# topdown 방식

import sys

N, K = map(int, sys.stdin.readline().split())
objects = []
for _ in range(N):
    w, v = map(int, sys.stdin.readline().split())
    objects.append((w, v))

objects.sort(key=lambda x:x[0])

dp = [0] + [-1] * K

def f(k, objects):
    if dp[k] != -1:
        return dp[k]
    
    candidates = [dp[k]]
    # print("k:", k, 'objects:', objects)

    for idx in range(len(objects)):
        # print("k:", k, 'idx = ', idx)

        weight, value = objects[idx]
        if k - weight < 0:
            break

        objects2 = objects.copy()
        objects2.pop(idx)

        # print(f'k : {k}, objects idx - {idx} popped.')
        candidates.append(f(k-weight, objects2) + value)

    dp[k] = max(candidates)
    return dp[k]

print(f(K, objects))