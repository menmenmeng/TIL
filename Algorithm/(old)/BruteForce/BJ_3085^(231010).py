N = int(input())
lines = []
for _ in range(N):
    line = list(input())
    lines.append(line)


def get_col_line(lines, col_idx):
    res = []
    for i in range(N):
        res.append(lines[i][col_idx])
    return res


def get_row_line(lines, row_idx):
    return lines[row_idx]


def get_max_num_candies(line):
    bf_candy = line[0]
    candies = [1] * N

    for i in range(1, N):
        if bf_candy==line[i]:
            candies[i]+=candies[i-1]
        
        bf_candy = line[i]
    
    return max(candies)


def change_blocks(row_id, col_id, side):
    if side == 'col':
        lines[row_id][col_id], lines[row_id][col_id+1] = lines[row_id][col_id+1], lines[row_id][col_id]
    elif side == 'row':
        lines[row_id][col_id], lines[row_id+1][col_id] = lines[row_id+1][col_id], lines[row_id][col_id]


max_candies = 1

for row_id in range(N):
    for col_id in range(N):
        if col_id<N-1 and lines[row_id][col_id]!=lines[row_id][col_id+1]:
            change_blocks(row_id, col_id, 'col')
            for i in range(N):
                max_candies = max(max_candies, get_max_num_candies(get_row_line(lines, i)))
                max_candies = max(max_candies, get_max_num_candies(get_col_line(lines, i)))
            change_blocks(row_id, col_id, 'col')

        if row_id<N-1 and lines[row_id][col_id]!=lines[row_id+1][col_id]:
            change_blocks(row_id, col_id, 'row')
            for i in range(N):
                max_candies = max(max_candies, get_max_num_candies(get_row_line(lines, i)))
                max_candies = max(max_candies, get_max_num_candies(get_col_line(lines, i)))
            change_blocks(row_id, col_id, 'row')

print(max_candies)