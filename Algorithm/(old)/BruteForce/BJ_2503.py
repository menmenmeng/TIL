'''
itertools의 permutations를 활용하여 순열의 모든 가짓수에서 하나씩 빼기.
'''
from itertools import permutations

num_list = list(permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)) # 모든 경우의 수

N = int(input())
for _ in range(N):
    target, s, b = list(map(int, input().split()))
    
    len_num_list = len(num_list)
    next_num_list = num_list.copy()

    # 각 자리의 숫자(int)로 이루어진 길이 3의 list로 변환
    target = list(map(int, list(str(target))))

    for idx_num in range(len_num_list):
        s_cnt = b_cnt = 0

        compare_num = num_list[idx_num]
        
        for char in target:
            if char in compare_num:
                if target.index(char) == compare_num.index(char):
                    s_cnt += 1
                else:
                    b_cnt += 1
        
        if s_cnt!=s or b_cnt!=b:
            next_num_list.remove(compare_num)
    
    num_list = next_num_list

print(len(num_list))


'''
정답 코드
문제점 : 두번째 for문의 기준이 되는 range(len(num))이 있는데, 그 for문 안에서 num.remove(num[i])라는 코드가 있음. 이 경우에 for문의 실행은 어떻게 되는지?

import sys
from itertools import permutations

n = int(input())
num = list(permutations([1,2,3,4,5,6,7,8,9], 3)) //미리 넣어놓는다.

for _ in range(n):
    test, s, b = map(int, input().split())
    test = list(str(test))
    remove_cnt = 0

    for i in range(len(num)):
        s_cnt = b_cnt = 0
        i -= remove_cnt

        for j in range(3):
            test[j] = int(test[j])
            if test[j] in num[i]:
                if j == num[i].index(test[j]):
                    s_cnt += 1
                else:
                    b_cnt += 1
    
        if s_cnt != s or b_cnt != b:
            num.remove(num[i])
            remove_cnt += 1

print(len(num))
출처: https://jainn.tistory.com/36 [Dogfootruler Kim:티스토리]
'''