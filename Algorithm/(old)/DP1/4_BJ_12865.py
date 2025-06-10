import sys

N, K = map(int, sys.stdin.readline().split())
objects = []
for i in range(N):
    W, V = map(int, sys.stdin.readline().split())
    objects.append((W, V))

objects.sort(key=lambda x:x[0])


max_values = [-1] * (K+1)
lightest_obj_w, lightest_obj_v = objects[0]
for i in range(lightest_obj_w):
    max_values[i] = 0
max_values[lightest_obj_w] = lightest_obj_v

def get_max_value(weight):
    if weight <= lightest_obj_w:
        return max_values[weight]
    
    max_candidates = []
    for obj_w, obj_v in objects:
        if weight - obj_w < 0:
            break
        elif max_values[weight - obj_w] >= 0:
            val = max_values[weight - obj_w]
        else:
            val = get_max_value(weight - obj_w)
            max_values[weight - obj_w] = val

        max_candidates.append(val + obj_v)
    
    max_values[weight] = max(max_candidates)
    return max_values[weight]

print(get_max_value(K))