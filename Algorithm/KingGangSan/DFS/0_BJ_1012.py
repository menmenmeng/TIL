# DFS 활용해서 혼자서 풀어보고, 그 다음
# 다른 사람들의 정답을 확인해보기.

T = int(input()) # test case number
worms_list = []
for _ in range(T):
    M, N, K = map(int, input().split()) # 가로, 세로, 배추개수.

    # 배추가 심어져 있는 곳
    vertices = []
    for _ in range(K):
        a, b = map(int, input().split())
        vertices.append((a, b))  # 여기까지 입력 받는 코드

    # 1. DFS를 재귀 없이, list만 사용해서 풀어 보기.
    visited_overall = []
    worms = 0
    for n in range(N): # 모든 좌표에 대해 검색해보자.
        for m in range(M):
            if (m, n) in visited_overall: # (m, n)좌표를 이미 visit 했다면.
                continue

            elif (m, n) not in vertices: # 방문하지 않았지만, vertices(배추) 목록엔 없을 때
                continue
                # visited_overall 목록과 관련 없는 데이터이므로 넘어가.
            
            else: # 방문하지 않았는데 배추 목록엔 있음.
                worms += 1

                # 지금 발견한 연결 리스트에 대해, visited와 need visit 리스트를 빈 값으로 놔둔다.
                # visited : 현 시점 연결 리스트의 visited 정보
                # stack : 현 시점 연결 리스트의 need_visit 정보
                visited, stack = [], [(m, n)]  # 시작점 정보.

                while stack: # need_visit_stack에 있는 데이터가 없어질 때까지, 계속 진행
                    # 0. stack의 마지막 노드를 현재 보고 있는 노드로 주기. (pop을 통해, stack에서는 제외)
                    # 1. 현재 노드를 visited에 추가
                    # 1-1. 현재 노드의 인접 노드 중, 전체 vertice에 있으면서, visited에는 없는 넘들 목록을 만들어서 stack에 추가
                    
                    current_node = stack.pop()

                    visited_overall.append(current_node) # (m, n) 좌표는 이제 visit 했다고 알려주기.
                    visited.append(current_node)

                    x, y = current_node
                    # 인접 노드들 목록.
                    adj_nodes = [
                        (adj_x, adj_y) for adj_x, adj_y in [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
                        if ( (adj_x, adj_y) in vertices ) and ( (adj_x, adj_y) not in visited )
                    ]
                    stack.extend(adj_nodes)
                    # print(stack) # for debug

    worms_list.append(worms)

for num in worms_list:
    print(num)


# 요약
# 연결 리스트를 순회할 때 필요한 list 두 개
# visited(방문한 노드인지 아닌지), need_visit(인접 노드를 계속 추가하는 stack)


import sys
sys.setrecursionlimit(100000)

T = int(input()) # test case number
worms_list = []
for _ in range(T):
    M, N, K = map(int, input().split()) # 가로, 세로, 배추개수.

    # 배추가 심어져 있는 곳
    vertices = []
    for _ in range(K):
        a, b = map(int, input().split())
        vertices.append((a, b))  # 여기까지 입력 받는 코드

    # dfs를 재귀함수 형태로 풀어보기
    # 필요한 것 : 연결 정보와 visited 정보. stack은 함수로서 해결 가능
    visited_overall = []
    worms = 0

    # dfs 재귀함수
    def dfs(vertices, current_node, visited):
        visited.append(current_node)
        x, y = current_node
        adj_nodes = [
            (adj_x, adj_y) for adj_x, adj_y in [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
            if ( (adj_x, adj_y) in vertices ) and ( (adj_x, adj_y) not in visited )
        ]
        for adj_node in adj_nodes:
            dfs(vertices, adj_node, visited)
        
        return visited


    for n in range(N): # 모든 좌표에 대해 검색해보자.
        for m in range(M):
            current_node = (m, n)
            if (current_node not in visited_overall) and (current_node in vertices):
                visited_overall.extend(dfs(vertices, current_node, []))
                worms += 1


    worms_list.append(worms)

for num in worms_list:
    print(num)
