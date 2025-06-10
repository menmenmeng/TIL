from collections import deque

n = int(input()) # num of all people
target_x, target_y = map(int, input().split())
m = int(input())
conn = [[] for _ in range(n+1)]
for _ in range(m):
    x, y = map(int, input().split())
    conn[x].append(y)
    conn[y].append(x)
    # 여기까지 입력

print(conn)


need_visit = deque()
need_visit.append(target_x)

visited = []

nums = [0] * (n+1)

while need_visit:
    _x = need_visit.popleft()
    print(_x)

    visited.append(_x)
    for con in conn[_x]:
        if con not in visited:
            need_visit.append(con)
            nums[con] = nums[_x] + 1
    print(need_visit)
    print(nums)

if nums[target_y] > 0:
    print(nums[target_y])
else:
    print(-1)