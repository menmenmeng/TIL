'''
문제 이해를 잘못함.
모든 회의가 들어갈 수 있도록 하는 최소의 회의실 개수를 구하라는 줄..
하나의 회의실 안에 최대한 많은 회의가 들어갈 수 있도록 할 때, 최대 회의 수를 구하는거다.
역시 문제를 잘 읽어야 한다.
'''

# N = int(input())
# startTimes = []
# endTimes = []
# durations = []
# for i in range(N):
#     startTime, endTime = map(int, input().split())
#     startTimes.append((i, startTime))
#     endTimes.append((i, endTime))
#     durations.append((i, endTime-startTime))

# first_startTime = min(startTimes, key=lambda x:x[1])[1]
# last_endTime = max(endTimes, key=lambda x:x[1])[1]

# durations.sort(key=lambda x:x[1], reverse=True)
# for idx, _ in durations:
#     startTime = startTimes[idx]
#     endTime = endTimes[idx]
