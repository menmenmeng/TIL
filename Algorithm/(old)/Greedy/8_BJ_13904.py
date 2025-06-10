N = int(input())
hws = []
for _ in range(N):
    d, w = map(int, input().split())
    hws.append((d, w))

hws.sort(key=lambda x:x[0])

dues = []
scores = []
for d, w in hws:
    dues.append(d)
    scores.append(w)

max_due_date = dues[-1] # 가장 마지막 due date. 6
res = 0
pos_dues = []

for day in range(max_due_date): # 0, 1, 2, 3, 4, 5
    pos_dues.append(max_due_date-day)
    # print(pos_dues)
    # print(dues)
    # print(scores)
    day_max_score = 0
    day_max_idx = -1
    for due_idx in range(len(dues)):
        due = dues[due_idx]
        score = scores[due_idx]
        if due in pos_dues:
            if score>day_max_score:
                day_max_score = score
                day_max_idx = due_idx

    if day_max_idx>=0: # 이게 문제였죠? -1보다 커야 하니까 >0 이 아니라 >=0 이어야 했음.
        res += day_max_score
        dues.pop(day_max_idx)
        scores.pop(day_max_idx)
        # print(max_idx, max_score, res)

print(res)