T = int(input())
test_case_answers = []

for _ in range(T):
    M, N, K = map(int, input().split())

    bachus = []
    for _ in range(K):
        bachus.append(tuple(map(int, input().split())))

    res = 0

    visited_overall = []
    for m in range(M):
        for n in range(N):
            if (m, n) in visited_overall:
                continue

            if (m, n) not in bachus:
                continue

            else:
                res += 1
                # 여기서부터, DFS로 탐색.
                # 1. 완전탐색 하다가 배추가 나오면, 그래프 서치를 한다.
                # 2. 그래프가 전부 DFS로 탐색될 때까지 기다리고, 탐색되고 나면 다시 vertice를 돈다.
                # 3. 그래프가 DFS로 탐색될때마다, 그 vertex를 visited_overall에 넣는다.
                
                need_visited=[(m, n)]
                visited = []
                while need_visited:
                    _m, _n = need_visited.pop()
                    visited_overall.append((_m, _n))
                    visited.append((_m, _n))
                    need_visited.extend([
                        pair for pair in [(_m, _n+1), (_m, _n-1), (_m+1, _n), (_m-1, _n)] 
                        if (pair in bachus) and (0 <= pair[0] < M) and (0 <= pair[1] < N)
                        and pair not in visited
                    ])

    test_case_answers.append(res)

for answer in test_case_answers:
    print(answer)