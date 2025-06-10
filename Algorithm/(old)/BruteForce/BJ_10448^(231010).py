N = int(input())

triangle_nums = []
for n in range(1, 50):
    triangle_nums.append(int(n*(n+1)/2))

answer_sheet = [0] * 1001

length = len(triangle_nums)
for i in range(length):
    for j in range(i, length):
        for k in range(j, length):
            num1 = triangle_nums[i]
            num2 = triangle_nums[j]
            num3 = triangle_nums[k]
            if num1 + num2 + num3 <= 1000:
                answer_sheet[num1+num2+num3] = 1

res = []

for _ in range(N):
    res.append(answer_sheet[int(input())])

for r in res:
    print(r)