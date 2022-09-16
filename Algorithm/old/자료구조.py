# DFS, BFS 전에 stack과 queue에 대한 이해가 기본적으로 되어 있어야.
# stack
# 선입후출(후입선출), FILO, LIFO
# stack 사용할 때는 그냥 list 쓰면 됨.
stack = []
stack.append(5)
stack.append(2)
stack.append(3)
stack.append(7)
stack.pop()
stack.append(1)
stack.append(4)
stack.pop()

print(stack)
print(stack[::-1])

# queue
# 선입선출, FIFO
# collections 라이브러리에서 deque 자료구조를 활용한다.
# deque는 스택과 큐의 장점을 모두 채택한 것. 데이터를 넣고 빼는 속도가 리스트 자료형에 비해 효율적이다.
from collections import deque

queue = deque()
queue.append(5)
queue.append(2)
queue.append(3)
queue.append(7)
queue.popleft()
queue.append(1)
queue.append(4)
queue.popleft()

print(queue)
queue.reverse()
print(queue)

# deque 객체를 list로 바꾸려면 list()메서드를 사용하자. list(queue) 가 이 코드에서 사용되어야

# 재귀 함수 
# 재귀 함수의 종료를 할 때는 return을 사용할 수 있음.

# DFS : stack을 활용함
# 1. 시작 노드를 stack에 삽입하고 방문 처리
# 2. 인접 노드를 스택에 방문 처리, 방문하지 않은 인접 노드가 없으면 스택에서 최상단 노드를 꺼냄(자식이 있는지)

# BFS : queue를 활용함.
