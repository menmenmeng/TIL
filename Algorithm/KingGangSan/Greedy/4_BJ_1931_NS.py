'''
한 개의 회의실 -> 사용하고자 하는 N개 회의에 대해, 회의실 사용표를 만든다.
각 회의는 시작시간, 끝나는 시간이 주어짐. 겹치지 않게 하면서, 회의실을 사용할 수 있게 하는 회의 최대 개수를 찾자.
회의는 시작하자마자 끝날 수도 있으며,
한 번 시작하면 중간에 중단될 수 없다.

그냥 제일 많이 겹치는 회의를 빼버리면 될 거 같다. 

제일 많이 겹치는 회의를 어떻게 알지? 이걸 어떻게 계산해야 하지.

'''

# 내 답(메모리 초과)
'''
N = int(input())
confs = []
for _ in range(N):
    sT,  eT = map(int, input().split())
    confs.append(set([i for i in range(sT, eT)]))

conf_reps = [0]*N # 몇 개 겹치는지
conf_infos = [] # 겹치는 놈들의 index가 뭔지.
for _ in range(N):
    conf_infos.append([])


# 아래 꺼 안됨. 왜 안되냐? [[]] * N이라고 하면, 같은 id의 빈 리스트를 N개 붙인 리스트를 리턴한다. 즉, 메모리 주소가 같음........... 진짜 쉽지 않다 파이썬

# conf_infos = [[]]*N # 겹치는 놈들의 index가 뭔지. #############
######
# [[]] * N --> 똑같은 id를 N개 붙여놓는다...... ㅠㅠㅠㅠㅠㅠㅠㅠ

for i in range(N): # N개를 다 돌면서, 각 i마다 겹치는 놈들의 index가 누구이고, 몇 개 겹치는지.
    conf = confs[i].copy() # confs중에서 하나를 가져온다. # 이거도 copy()안 하면 어떻게 되나.
    remained_range = list(range(N)) # 0~N-1
    remained_range.remove(i) # 위에 중에서 i를 제외한 나머지들의 리스트.
    for k in remained_range: # i를 제외한 나머지 중에서.
        if len(conf.intersection(confs[k]))>0: # 만약 겹치는 부분이 있다면.
            conf_reps[i]+=1 # reps의 i index부분에 1을 추가해주고.
            conf_infos[i].append(k) # infos의 i index에 있는 


res = N
while True:
    max_rep = max(conf_reps) # 몇 개 겹치는지 리스트에서 가장 큰 값(얘 없앨 거임)
    if max_rep == 0:
        break

    max_idx = conf_reps.index(max_rep) # 몇 개 겹치는지 리스트에서 가장 큰 값의 index
    res -= 1 # 결과값에서 1을 빼줘
    for i in range(N): # 모든 N개 회의에 대해서
        conf_info = conf_infos[i].copy() # 할당해서 새로운 list 만들자.
        if max_idx in conf_info: # 겹치는 놈들의 index 리스트 안에, max_idx있어?
            conf_infos[i].remove(max_idx) # 있으면 거기서 없애
            conf_reps[i] -= 1 # conf_reps에서도 없애.
    conf_reps[max_idx] = 0 # 마지막으로, conf_reps에서 max_idx의 값을 0으로 만들어 버려.
print(res)

'''
# 위의 답처럼 하면 메모리 초과 오류가 납니다......


'''
앞에서부터, 제일 빨리 끝나는 순서대로 채워간다고 하면.
어떻게 된다? 채워간다고 하면 -- 가장 많은 회의를 가지게 된다.
왜?
어쨌든, 맨 처음에 올 회의를 정하려면. 맨 처음에 올 수 있는 다양한 (겹치는) 회의들 중에 하나를 가져가야 한다. 그치?
그러면. 뭐가 됐든 간에 맨 처음에 올 수 있는 회의를 정할 건데, 뒤에 있는 회의가 더 많이 고려되길 원한다면
당연히 먼저 끝나는 걸 우선으로 가져가야 하는거지.
'''