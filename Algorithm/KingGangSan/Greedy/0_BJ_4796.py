'''
등산가 김강산은 가족들과 함께 캠핑을 떠났다. 하지만, 캠핑장에는 다음과 같은 경고문이 쓰여 있었다.

캠핑장은 연속하는 20일 중 10일동안만 사용할 수 있습니다.

강산이는 이제 막 28일 휴가를 시작했다. 이번 휴가 기간 동안 강산이는 캠핑장을 며칠동안 사용할 수 있을까?

강산이는 조금 더 일반화해서 문제를 풀려고 한다. 

캠핑장을 연속하는 P일 중, L일동안만 사용할 수 있다. 강산이는 이제 막 V일짜리 휴가를 시작했다. 강산이가 캠핑장을 최대 며칠동안 사용할 수 있을까? (1 < L < P < V)


예제 입력
5 8 20
5 8 17
0 0 0
예제 출력
Case 1: 14
Case 2: 11
'''

i = 0
res = []
while True :
    i += 1
    L, P, V = map(int, input().split())
    if not (L or P or V) :
        break

    max_num = V//P
    remained_days = V - V//P*P
    ans = max_num * L + min(remained_days, L)
    res.append(f'Case {i}: {ans}')

for answer in res:
    print(answer)