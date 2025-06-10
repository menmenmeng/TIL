N = int(input())
nums = list(map(int, input().split()))

'''
다시 생각해본 것.
앞에서부터 계속해서 부분합을 구한다.
부분합을 구하다가, 부분합이 음수가 되면 다음 부분합 구할 땐 그냥 이전 부분합을 더하지 말고 간다 --> 0으로 놓자.
부분합을 구하다가, 부분합이 음수가 되면 그냥 그 부분합 자리는 0으로 만들어버린다. --> 이거의 문제는, 
'''
# best = nums[0]
# for i in range(1, N):
#     if nums[i-1]>=0:
#         nums[i]+=nums[i-1]
    
#     best = max(best, nums[i])

# print(best)

best = nums[0]
nums = [-9999] + nums
for i in range(1, N+1):
    if nums[i-1]<0:
        nums[i-1] = 0

    nums[i] += nums[i-1]

    best = max(best, nums[i])

print(best)