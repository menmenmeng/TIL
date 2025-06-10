N = int(input()) # 센서 개수
K = int(input()) # 집중국 개수
if K>N :
    print(0)
else:
    sensors = list(map(int, input().split())) # 센서의 좌표
    sensors.sort()
    if K==1:
        print(sensors[-1]-sensors[0])
    else:
        sensors_diff = []
        for i in range(1, N):
            p = sensors[i]
            q = sensors[i-1]
            sensors_diff.append(p-q)

        sensors_diff.sort()
        print(sum(sensors_diff[:-(K-1)]))