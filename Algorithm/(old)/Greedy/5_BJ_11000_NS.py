'''
N = int(input())
classes = []
for _ in range(N):
    s, e = map(int, input().split())
    classes.append([s, e])

classes.sort(key=lambda x:x[1])
classes.sort(key=lambda x:x[0])

res = [classes[0][1]] # 첫 번째 강의실이 끝나는 시간
for i in range(1, N):
    cls_start, cls_end = classes[i] # 두 번째부터, 강의가 끝나는 시간 대입
    # 만약 강의가 시작하는 시간이, res에 들어있는 강의실이 끝나는 시간보다 크거나 같다면.
    if res[0] <= cls_start:
        # 그럴 땐, res의 맨 첫번째 강의실을 이 강의가 끝나는 시간으로 교체하고.
        res[0] = cls_end
        # 그다음에, res를 sort한다. 작은 거에서부터.
        res.sort()
    else: # 만약, 강의가 시작하는 시간이 res에 들어있는 강의실이 끝나는 시간보다 작다면.
        res.append(cls_end)
        res.sort()

print(len(res))
'''
## 위의 풀이가 안 되는 이유? heapq를 쓰지 않았기 때문....
# python heapq를 사용해 보자.

import heapq

N = int(input())
classes = []
for _ in range(N):
    s, e = map(int, input().split())
    classes.append([s, e])

classes.sort(key=lambda x:x[1])
classes.sort(key=lambda x:x[0])

res = [classes[0][1]] # heap 자료구조로 사용될 것.

for i in range(1, N):
    cls_start, cls_end = classes[i] # 두 번째부터, 강의가 끝나는 시간 대입
    # 만약 강의가 시작하는 시간이, res에 들어있는 강의실이 끝나는 시간보다 크거나 같다면.
    if res[0] <= cls_start:
        # 그럴 땐, res의 맨 첫번째 강의실을 이 강의가 끝나는 시간으로 교체하고, 새 cls를 집어넣는다.
        heapq.heappop(res)
        heapq.heappush(res, cls_end)

    else: # 만약, 강의가 시작하는 시간이 res에 들어있는 강의실이 끝나는 시간보다 작다면.
        heapq.heappush(res, cls_end)

print(len(res))

# heapq를 활용한 구현은 과연 성공할까? -> 이것도 시간초과 뜨는데요....