# heapq 사용해서, 우선순위 큐 사용해서 문제 다시 풀어보기. 231012에...목금토. 
'''
풀이방법.

시작순서로 놔두고. classes에는 끝나는 시간을 담는다.
'''
import heapq
import sys

N = int(input())
lessons = []
for _ in range(N):
    startTime, endTime = map(int, sys.stdin.readline().split())
    lessons.append((startTime, endTime))

lessons.sort(key=lambda x:x[0])

classes_endtimes = [lessons[0][1]] # 최초의 class endtime

for startTime, endTime in lessons[1:]:
    heapq.heappush(classes_endtimes, endTime)
    min_endtime = heapq.heappop(classes_endtimes)
    if min_endtime > startTime:
        heapq.heappush(classes_endtimes, min_endtime)
        

print(len(classes_endtimes))