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

#     numbers = [0] + list(map(int, input().split()))
#     visited = [True] + [False] * n

#     res = n
#     for i in range(1, n+1): # 모든 학생들에 대해서.
#         if visited[i]:
#             continue
#         else:
#             current = i
#             next_student = numbers[current]
#             tmp_team = [current]
#             visited[i] = True
#             while not visited[next_student]:
#                 next_student = numbers[current]
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

'''
Test Case
2                   # number of test case
7                   # test#1 : student number
3 1 3 7 3 4 6       # test#1 : numbers info
8                   # test#2 : student number
1 2 3 4 5 6 7 8     # test#2 : numbers info
'''


# T = int(input())

# test_case_results = []

# for _ in range(T):
#     n = int(input())
#     numbers = [0] + list(map(int, input().split()))
#     visited_overall = [True] + [False] * n

#     test_team = []

#     for i in range(1, n+1):
#         if visited_overall[i]:
#             continue

#         nxt = i
#         visited_idx = [False] * (n+1)
#         visited = []

#         while True:
#             crr = nxt
#             if visited_overall[crr]:
#                 break

#             nxt = numbers[crr]
#             visited_idx[crr] = True
#             visited.append(crr)
#             visited_overall[crr] = True

#             if visited_idx[nxt]:
#                 idx = visited.index(nxt)
#                 team = visited[idx:]
#                 test_team.extend(team)
#                 break

#     res = n - len(test_team)
#     test_case_results.append(res)

# for r in test_case_results:
#     print(r)



# 함수로 구현해 보자.
