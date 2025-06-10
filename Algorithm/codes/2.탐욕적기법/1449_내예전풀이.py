N, L = map(int, input().split()) # 4, 2
leaks = list(map(int, input().split())) # [1, 2, 100, 101]
leaks.sort()
res = 0

pointer_value = leaks[0] # 1, 2, 100, 101
for i in range(N):
    leaks[i] -= pointer_value # 물이 뚫린 곳 사이의 길이를 재는 거랑 같다. 최초 pointer와 물이 뚫린 곳을 계속 비교했을 때 
    if leaks[i] >= L:
        res += 1
        pointer_value += leaks[i]
res += 1

print(res)