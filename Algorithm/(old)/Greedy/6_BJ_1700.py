# 시간제한 2초 -> 2억번
# 메모리제한 128MB
# 뒤에 또 쓸 일이 "적게 남은" 걸 먼저 뺀다. 이게 최적의 해가 될 것 같음

# 첫 번째 답(틀림)
'''
N, K = map(int, input().split())
order = list(map(int, input().split())) # K개

space = [] # N개
res = 0 # 플러그 뽑는 횟수.
for idx in range(K):
    dev = order[idx]
    if dev in space: # space 내에 device 가 있다면,
        continue # 아무 일도 하지 말고 그대로 지나가라.
    else : # 만약 space 내에 device가 없다면, 두 가지 경우다.
        # 첫 번째, space를 아직 다 사용하지 않은 상태에서 device가 없음
        if len(space) < N:
            space.append(dev) # 그 경우, device를 그냥 space에 추가해 주면 된다.
        elif len(space) == N: # 만약, len(space) 가 N 이다.
            future_needs = []
            for s_dev_idx in range(N): # 지금 space내의 idx
                s_dev = space[s_dev_idx] # space idx를 가진 device를 s_dev라고 하자.
                future_need = order[idx+1:].count(s_dev) # s_dev가 지금의 idx 뒤에 몇 개 있는가? 
                future_needs.append(future_need)
                # current num이 가장 작은 s_dev를 뽑아야 한다.
            try:
                min_index = future_needs.index(min(future_needs)) # future_need가 min 값을 가진 index를 특정하여.
            except:
                min_index = 0

            try:
                space.pop(min_index) # space에서 뽑는다.
                res += 1 # 플러그 뽑는 횟수를 하나 더해준다.
                # 그 다음, space에 현재 device를 추가한다.
            except:
                pass
            
            space.append(dev)

print(res)
'''


# 두 번째 답 (틀림)
'''
N, K = map(int, input().split())
order = list(map(int, input().split())) # K개

space = [] # 콘센트 개수 N개. 즉 len(space)의 최댓값은 N이다. 그 이상으로 갈 수는 없음!
res = 0 # 플러그 뽑는 횟수. 뽑을 때마다 1씩 추가

# 알고리즘: (for) 사용할 플러그 리스트를 돌면서, 
# (if) space 안에 지금 사용하고 싶은 플러그가 꽂혀 있다면
## pass
# (if) space의 개수가 N개보다 적다면
## 그냥 space에 새로운 플러그를 꽂아 준다
# (if) space의 개수가 N개이며, + space 안에 지금 사용하고 싶은 플러그가 꽂혀 있지 않다면.
## 미래에 사용할 횟수가 가장 낮은 플러그를 뽑고, space에 지금 사용할 플러그를 꽂는다

for idx in range(K):
    plug = order[idx] # 현재 사용하려는 plug의 번호
    if plug in space: # space안에 plug가 이미 있다면.
        # print(plug, space) # debug
        pass
    elif len(space)<N: # space 안에 plug가 없지만, len_space가 N보다 작다면.
        space.append(plug) # 그냥 append만 해
        # print(plug, space) # debug
    elif len(space)==N: # space 안에 plug가 없고, len_space가 N이라면. (굳이 plug not in space조건을 쓸 이유가 없다. 왜냐하면, elif로 제외되었음)
        future_needs_of_using_plugs = [] # using plug들의 future need를 space 내에 담긴 index 순서대로 담는다.
        if idx==K-1:
            space.pop()
            res += 1
            space.append(plug)
            # print(plug, space) # debug
        else:
            future_plug = order[idx+1:] # 지금부터 이후까지.
            for using_plug in space: # space 내에 이미 있는 using plug중에서.
                future_needs_of_using_plugs.append(future_plug.count(using_plug))
            min_need = min(future_needs_of_using_plugs) # min_need가 가장 작은 것이 무엇인지를 보겠다.

            future_min_count = future_needs_of_using_plugs.count(min_need)
            if future_min_count>1: # min_need가 가장 작은 것이 여러 개 있다면.
                future_needs_same = [] # space내에서, future_need가 same인 index들을 모아줄 것.
                for _ in range(future_min_count):  # min_need 개수만큼 추가할 거다.
                    pop_plug_index_space = future_needs_of_using_plugs.index(min_need) # min_need를 가진 첫 요소의 index (in space)
                    future_needs_same.append(pop_plug_index_space) # 인덱스를 future_needs_same에 넣어준다.
                    future_needs_of_using_plugs[pop_plug_index_space] = -future_needs_of_using_plugs[pop_plug_index_space]
                    # future_needs of using plugs 리스트의 그 숫자를 음수로 만들어줘서, 다음 index 체크할 때 pass하도록 함.

                # 그래서 그 index에 따른 using plug는?
                same_needs_using_plugs = [space[idx] for idx in future_needs_same]
                # 이제 이 중에서 가장 마지막에 나오는 놈이 누군지를 알아야 함.
                for j in range(K):
                    dev = order[::-1][j]
                    if dev in same_needs_using_plugs: # 만약 dev가 가장 먼저 나왔다. 그러면 dev를 빼면 된다.
                        space.remove(dev)
                        res += 1
                        space.append(plug)
                        # print(plug, space)
                        break # for문 탈출

            else: # 하나면. 
                pop_plug_index_space = future_needs_of_using_plugs.index(min_need)
                space.pop(pop_plug_index_space)
                res += 1
                space.append(plug)
                # print(plug, space) # debug

print(res)
'''

# 정답
N, K = map(int, input().split())

multitap = list(map(int, input().split())) # 멀티탭 사용할 순서

plugs = []
count = 0

for i in range(K):
    # 있으면 건너 뛴다.
    if multitap[i] in plugs: # 사용하는 콘센트에 멀티탭 현재 순서가 있다면.
        continue
  
  # 플러그가 1개라도 비어 있으면 집어넣는다.
    if len(plugs) < N:
        plugs.append(multitap[i])
        continue
  
    multitap_idxs = [] # 다음 멀티탭의 값을 저장.
    hasplug = True

    for j in range(N): # 사용하는 멀티탭의 개수대로. 즉 멀티탭 하나씩 돌아가면서 확인할 예정.
  	    # 멀티탭 안에 플러그 값이 있다면
        if plugs[j] in multitap[i:]: # 멀티탭의 현재 index에서부터 마지막까지를 가져와서. 기존 사용중인 plug를 또 사용할 건지 확인(i나 i+1이나 관계X)
            # 멀티탭 인덱스 위치 값 가져오기.
            multitap_idx = multitap[i:].index(plugs[j]) # 기존 사용중인 plug가 나중에 또 사용된다면, 언제 사용될건지 index를 가져온다.
        else:
            multitap_idx = 101 # 만약 사용 안한다면, 101을 가져온다.
            hasplug = False # 아 왜냐면 얘를 빼면 되니까. 사용 안한다 그러면 얘를 빼면 되니까

        # 인덱스에 값을 넣어준다.
        multitap_idxs.append(multitap_idx) # 위에서 계산한, 언제 사용할건지와 관련된 index를 multitap_idxs에 넣어준다.
    
        # 없다면 종료
        if not hasplug:
            break # 왜 여기서 break를.>?
  
    # 플러그를 뽑는다.
    plug_out = multitap_idxs.index(max(multitap_idxs))
    del plugs[plug_out] # 플러그에서 제거
    plugs.append(multitap[i]) # 플러그에 멀티탭 값 삽입
    count += 1 # 뽑았으므로 1 증가

print(count)


### 정답 이유 : 미래에 없거나, 가장 마지막에 나오는 애를 먼저 뽑아주면 된다. 미래 순서에 몇 번 나올지랑은 관계가 없음...........맞네. 