"""
문제
N×N크기의 행렬로 표현되는 종이가 있다. 종이의 각 칸에는 -1, 0, 1 중 하나가 저장되어 있다. 우리는 이 행렬을 다음과 같은 규칙에 따라 적절한 크기로 자르려고 한다.

만약 종이가 모두 같은 수로 되어 있다면 이 종이를 그대로 사용한다.
(1)이 아닌 경우에는 종이를 같은 크기의 종이 9개로 자르고, 각각의 잘린 종이에 대해서 (1)의 과정을 반복한다.
이와 같이 종이를 잘랐을 때, -1로만 채워진 종이의 개수, 0으로만 채워진 종이의 개수, 1로만 채워진 종이의 개수를 구해내는 프로그램을 작성하시오.

입력
첫째 줄에 N(1 ≤ N ≤ 37, N은 3k 꼴)이 주어진다. 다음 N개의 줄에는 N개의 정수로 행렬이 주어진다.

출력
첫째 줄에 -1로만 채워진 종이의 개수를, 둘째 줄에 0으로만 채워진 종이의 개수를, 셋째 줄에 1로만 채워진 종이의 개수를 출력한다.
"""
from itertools import product

N = int(input())
matrix = []
for _ in range(N):
    row = list(map(int, input().split()))
    matrix.append(row)

res = [0, 0, 0]

def func(matrix, N, res):
    start = matrix[0][0]
    for row_idx, col_idx in product(range(N), repeat=2):
        if start != matrix[row_idx][col_idx]:
            break

    # break 수행되지 않았을 경우,
    else:
        res[start] += 1
        return res
    
    # break 수행시.
    matrices = []
    gap = N // 3

    # 9개의 matrix로 쪼개는 과정..
    for row_idx_start in range(0, N, gap):
        for col_idx_start in range(0, N, gap):
            temp_matrix = []
            for row_idx in range(row_idx_start, row_idx_start + gap):
                temp_row = []
                for col_idx in range(col_idx_start, col_idx_start + gap):
                    temp_row.append(matrix[row_idx][col_idx])
                temp_matrix.append(temp_row)
            matrices.append(temp_matrix) # 9개 matrix 만들어짐.

    for mat in matrices:
        res = func(mat, gap, res)
    
    return res

result = func(matrix, N, res)
print(result[-1])
print(result[0])
print(result[1])