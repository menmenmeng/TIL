# from collections import deque

# T = int(input()) # test case number

# test_case_results = []

# for _ in range(T):
#     n = int(input()) # number of students

#     students = [i for i in range(1, n+1)]
#     connect_info = dict()
#     arrows = map(int, input().split())

#     team_student = []
#     # 연결 정보 만들기.
#     for student, arrow in zip(students, arrows):
#         try:
#             connect_info[student].append(arrow)
#         except:
#             connect_info[student] = [arrow]

#     # student를 돌면서 dfs해서 만약 visit했던 node가 또 나온다면. 한 팀으로 친다.
#     visited_overall = []
#     for student in students:
#         if student in visited_overall:
#             continue
#         visited = []
#         need_visit = deque()
#         need_visit.append(student)
#         while need_visit:
#             current_node = need_visit.pop()
#             if current_node in visited_overall:
#                 break
#             if current_node in visited:
#                 idx = visited.index(current_node)
#                 tmp_team = visited[idx:]
#                 team_student.extend(tmp_team)
#                 break
#             visited.append(current_node)
#             visited_overall.append(current_node)
#             need_visit.extend(connect_info[current_node])
        
#     res = n - len(team_student)
#     test_case_results.append(res)

# for res in test_case_results:
#     print(res)

# 위에꺼 시간초과 뜸



# T = int(input()) # test case number

# test_case_results = []

# for _ in range(T):
#     n = int(input()) # number of students
#     # 연결 정보 만들기. # 연결 정보를 dictionary로 만들 필요가 없다. 애초에 학생이 1, 2, 3, .. 등 숫자로 이루어져 있음!!

#     connection = [0] + list(map(int, input().split()))
#     visited = [True] + [False] * n

#     res = n
#     for i in range(1, n+1): # 모든 학생들에 대해서.
#         if visited[i]:
#             continue
#         else:
#             current = i
#             next_student = connection[current]
#             tmp_team = [current]
#             visited[i] = True
#             while not visited[next_student]:
#                 next_student = connection[current]
#                 if next_student in tmp_team:
#                     res -= len(tmp_team[tmp_team.index(next_student):])
#                 else:
#                     tmp_team.append(next_student)
#                     visited[next_student] = True
#                     current = next_student

#     test_case_results.append(res)

# for res in test_case_results:
#     print(res)

# 위에꺼 시간초과 뜸
# 똑같은 로직인데 왜 내꺼만 시간초과 뜸...


T = int(input()) # test case number

test_case_results = []

for _ in range(T):
    n = int(input()) # number of students
    # 연결 정보 만들기. # 연결 정보를 dictionary로 만들 필요가 없다. 애초에 학생이 1, 2, 3, .. 등 숫자로 이루어져 있음!!
    connection = [0] + list(map(int, input().split()))
    visited_overall = [True] + [False] * n

    res = n

    for i in range(1, n+1):
        # 1. 이미 전체적으로 방문했던 학생이라면, 다시 할 필요 없다. continue
        # 2. 방문하지 않았던 학생이라면, 순회할 필요가 있다.
        # 2. 사이클이 만들어지는지를 확인해야 한다.
        # 2-0. 현재 학생을 시작으로 하는 cycle 리스트를 만든다.
            # 2-1. 다음 학생을 connection 리스트에서 가져온다. 반복해야 한다. 그냥 while True를 해도 될 듯. break 조건이 있으니
            # 2-2. 다음 학생이 order안에 있는지 확인한다.
                # 2-2-1. 만약 있다면, cycle이 만들어지는 것이므로 cycle을 끊어내서 학생수를 파악
                # 2-2-1. 학생 수를 파악한 뒤, n에서 이 수만큼 빼준다.
                # 2-2-1. 계산했다면 for문을 다시 돌러 가자.(break)
                # 2-2-2. 만약 없다면, cycle안에 학생을 넣어준다.
                # 2-2-2. 그리고 visited_overall의 학생 index에 True를 집어넣어준다.
            # 2-1 ~ 2-2-2를 반복한다.

        if not visited_overall[i]: # 방문한 학생노드가 아니라면.
            current_student = i
            next_student = connection[current_student]
            order = []

            while True:
                order.append(current_student)
                next_student = connection[current_student]
                if not visited_overall[next_student]:
                    
                else:
                    break



    test_case_results.append(res)

for r in test_case_results:
    print(r)