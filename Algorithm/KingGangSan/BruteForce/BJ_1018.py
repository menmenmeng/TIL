'''
지민이는 자신의 저택에서 MN개의 단위 정사각형으로 나누어져 있는 M×N 크기의 보드를 찾았다. 어떤 정사각형은 검은색으로 칠해져 있고, 나머지는 흰색으로 칠해져 있다. 지민이는 이 보드를 잘라서 8×8 크기의 체스판으로 만들려고 한다.

체스판은 검은색과 흰색이 번갈아서 칠해져 있어야 한다. 구체적으로, 각 칸이 검은색과 흰색 중 하나로 색칠되어 있고, 변을 공유하는 두 개의 사각형은 다른 색으로 칠해져 있어야 한다. 따라서 이 정의를 따르면 체스판을 색칠하는 경우는 두 가지뿐이다. 하나는 맨 왼쪽 위 칸이 흰색인 경우, 하나는 검은색인 경우이다.

보드가 체스판처럼 칠해져 있다는 보장이 없어서, 지민이는 8×8 크기의 체스판으로 잘라낸 후에 몇 개의 정사각형을 다시 칠해야겠다고 생각했다. 당연히 8*8 크기는 아무데서나 골라도 된다. 지민이가 다시 칠해야 하는 정사각형의 최소 개수를 구하는 프로그램을 작성하시오.

<시간제한>
2초


<개선>
W로 시작할 때와 B로 시작할 때, 나는 두 개를 for문을 이용해서 만들었다.
정답을 만든 사람들은 W로 시작할 때와 B로 시작할 때 각각을 더하는 변수를 새로 만들어서 활용했다.
'''

# 나의 답
# row, column = list(map(int, input().split()))
# board = []
# for r in range(row):
#     board.append(list(input()))


# first_index_list = []

# first_index_row_len = row - 8 + 1
# first_index_col_len = column - 8 + 1
# for r in range(first_index_row_len):
#     for c in range(first_index_col_len):
#         first_index_list.append([r, c])

# min_change_num = 64

# for ri, ci in first_index_list:
#     ## 정답 문제 풀이에서는 n을 두 개 지정했다. 하나는 B, 하나는 W를 담당하도록.
#     for first_color in ['B', 'W']:
#         n = 0
#         std_color = first_color
#         for dr in range(8):
#             for dc in range(8):
#                 if std_color != board[ri+dr][ci+dc]:
#                     n+=1
#                 else:
#                     pass
                
#                 if dc == 7:
#                     std_color = std_color
#                 else:
#                     if std_color == 'B':
#                         std_color = 'W'
#                     else:
#                         std_color = 'B'

#         min_change_num = min(n, min_change_num)

# print(min_change_num)


# 다시.
row, column = list(map(int, input().split()))
board = []
for r in range(row):
    board.append(list(input()))


first_index_list = []

first_index_row_len = row - 8 + 1
first_index_col_len = column - 8 + 1
for r in range(first_index_row_len):
    for c in range(first_index_col_len):
        first_index_list.append([r, c])

min_change_num = 64

for ri, ci in first_index_list:
    nB = 0
    nW = 0
    for dr in range(8):
        for dc in range(8):
            if (dr-dc)%2==1:
                if board[ri+dr][ci+dc] == 'B':
                    nB += 1
                else:
                    nW += 1

            else:
                if board[ri+dr][ci+dc] == 'B':
                    nW += 1
                else:
                    nB += 1

    min_change_num = min(nB, nW, min_change_num)

print(min_change_num)

