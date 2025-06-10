n = int(input()) # 전체 사람 수
target1, target2 = map(int, input().split()) # 촌수 계산할 두 사람

m = int(input()) # 연결 간선 수
connect_info = dict() # 연결 관계
for _ in range(m):
    x, y = map(int, input().split())

    try:
        connect_info[x].append(y)
    except:
        connect_info[x] = [y]

    try:
        connect_info[y].append(x)
    except:
        connect_info[y] = [x]

# target 1 ~ 2 , 연결관계까지 전부 scan했음. 이제, target 1에서 BFS해서 target2로 갈 수 있느냐 없느냐를 판단해야 한다.

# queue 이용하면 된다고 했다.

from collections import deque

def bfs(node):
    queue = deque()
    queue.append(node)
    while queue:
        node = queue.popleft()
        for n in graph[node]:
            if check[n] == 0:
                check[n] = check[node]+1
                queue.append(n)
            
n = int(input())
graph = [[] for _ in range(n+1)]
s, e = map(int, input().split())
for _ in range(int(input())):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)
check = [0]*(n+1)
bfs(s)
print(check[e] if check[e] > 0 else -1)