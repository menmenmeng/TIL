'''
<문제>
상근이는 어렸을 적에 "봄보니 (Bomboni)" 게임을 즐겨했다.

가장 처음에 N×N크기에 사탕을 채워 놓는다. 사탕의 색은 모두 같지 않을 수도 있다. 상근이는 사탕의 색이 다른 인접한 두 칸을 고른다. 그 다음 고른 칸에 들어있는 사탕을 서로 교환한다. 이제, 모두 같은 색으로 이루어져 있는 가장 긴 연속 부분(행 또는 열)을 고른 다음 그 사탕을 모두 먹는다.

사탕이 채워진 상태가 주어졌을 때, 상근이가 먹을 수 있는 사탕의 최대 개수를 구하는 프로그램을 작성하시오.

<시간제한>
1초

<예제>
입력
3
CCP
CCP
PPC
출력
3
'''
# 후보 1
# 존나게 길고 존나 비효율적이다.
'''
N = int(input())
board = []
for i in range(N):
    board.append(list(str(input())))

def check_h(board):
    maxnum = 1
    for row in board:
        temp_num = 1
        for i in range(1, N):
            if (row[i-1]==row[i]):
                temp_num += 1
            else:
                temp_num = 1
        if temp_num > maxnum:
            maxnum = temp_num

    return maxnum

def check_v(board):
    maxnum = 1
    for col_index in range(N):
        column = [row[col_index] for row in board]
        temp_num = 1
        for i in range(1, N):
            if (column[i-1]==column[i]):
                temp_num += 1
            else:
                temp_num = 1
        if temp_num > maxnum:
            maxnum = temp_num
    
    return maxnum

# 가로로 바꾸기
maxnum = 1
for v in range(N):
    for h in range(N-1):
        if board[v][h] != board[v][h+1]:
            board[v][h], board[v][h+1] = board[v][h+1], board[v][h]
            print(board)
            maxnum = max(check_h(board), check_v(board), maxnum)
            if maxnum == N:
                print(maxnum)
                quit()
            board[v][h], board[v][h+1] = board[v][h+1], board[v][h]

for h in range(N):
    for v in range(N-1):
        if board[v][h] != board[v+1][h]:
            board[v][h], board[v+1][h] = board[v+1][h], board[v][h]
            print(board)
            maxnum = max(check_h(board), check_v(board), maxnum)
            if maxnum == N:
                print(maxnum)
                quit()
            board[v][h], board[v+1][h] = board[v+1][h], board[v][h]
'''


# 후보 2
# 왜 답이 틀려...? 왜? 왜? 왜? 왜?
'''
N = int(input())
board = []
for i in range(N):
    board.append(list(str(input())))

def check_max(board):
    # row
    row_res = 1
    for row in board:
        row_max = [1]*N
        if row[i-1]==row[i]:
            row_max[i] += 1
        if row_res < max(row_max):
            row_res = max(row_max)

    # column
    col_res = 1
    for col_index in range(N):
        col = [row[col_index] for row in board]
        col_max = [1]*N
        if col[i-1]==col[i]:
            col_max[i] += 1
        if col_res < max(col_max):
            col_res = max(col_max)

    return max(row_res, col_res)

res = 1
quitFlag = 0
for ri in range(N):
    if quitFlag:
        break
    for ci in range(N):
        # 오른쪽
        try:
            board[ri][ci], board[ri][ci+1] = board[ri][ci+1], board[ri][ci]
            temp_max = check_max(board)
            board[ri][ci], board[ri][ci+1] = board[ri][ci+1], board[ri][ci]
            if temp_max > res:
                res = temp_max
            if res == N:
                quitFlag = 1
                break
        
        except:
            pass

        try:
        # 아래쪽
            board[ri][ci], board[ri+1][ci] = board[ri+1][ci], board[ri][ci]
            temp_max = check_max(board)
            board[ri][ci], board[ri+1][ci] = board[ri+1][ci], board[ri][ci]
            if temp_max > res:
                res = temp_max
            if res == N:
                quitFlag = 1
                break
        except:
            pass

        print(res)
print(res)
'''

import numpy as np
# 후보 3
# 후보1, 후보2 다 알고리즘은 똑같음. 그저 더 더러운 코드일 뿐
N = int(input())
board = []
for _ in range(N):
    board.append(list(str(input())))

def check(board):
    # row
    row_max = 1
    for i in range(N):
        row_cnt = 1
        for j in range(1, N):
            if board[i][j-1] == board[i][j]:
                row_cnt += 1
            else:
                row_cnt = 1
            row_max = max(row_max, row_cnt)

    # column
    col_max = 1
    for j in range(N):
        col_cnt = 1
        for i in range(1, N):
            if board[i-1][j] == board[i][j]:
                col_cnt += 1
            else:
                col_cnt = 1
            col_max = max(col_max, col_cnt)
    
    return max(row_max, col_max)

# 위치 바꾸면서 check
current_max = 1
for i in range(N):
    for j in range(N):
        try:
            if board[i][j] != board[i][j+1]:
                board[i][j], board[i][j+1] = board[i][j+1], board[i][j]
                # print(np.array(board), check(board), '\n')
                current_max = max(current_max, check(board))
                board[i][j], board[i][j+1] = board[i][j+1], board[i][j]
        except:
            pass

        try:
            if board[i][j] != board[i+1][j]:
                board[i][j], board[i+1][j] = board[i+1][j], board[i][j]
                # print(np.array(board), check(board), '\n')
                current_max = max(current_max, check(board))
                board[i][j], board[i+1][j] = board[i+1][j], board[i][j]
        except:
            pass

    if current_max == N:
        break

print(current_max)