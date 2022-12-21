# Coroutine
- 왜 공부중 ? 웹소켓에서 비동기 처리에 관련된 내용이 나왔기 때문이다.

~~~python
import asyncio
import websockers
~~~

위의 라이브러리 왜 사용하는지 알아보고 싶어서


## 루틴

- 컴퓨터 프로그램의 일부로써, 특정한 일을 실행하기 위한 일련의 명령이다.
--> 프로그래밍에서는 루틴이 곧 함수

## 서브루틴

- Sub routine : 루틴 안에 있는 부 루틴, 함수 안에서 서브로 실행되는 함수.

~~~python
def routine1():
    routine2()

def routine2():
    print("routine 2")
~~~

위 코드에서 routine2가 routine1의 서브루틴.

## 코루틴

- Co-routine : 같이 실행되는 함수.

하나의 스레드에서, 두 개의 루틴이 같이 실행되고 있다. --> coroutine1이 진행되던 도중, coroutine2가 나와야 하는 상황일 때 coroutine1을 잠깐 중단하고 coroutine2를 진행했다가 다시 coroutine1으로 돌아감.

--> 하나가 다른 하나의 sub개념이 아니라 한 스레드에서 함께 진행되는 루틴이다. : __비동기 프로그래밍__

## 동기 / 비동기 프로그래밍

### 동기 처리

특정 작업이 끝나면 다음 작업을 처리하는 __순차 처리 방식__

### 비동기 처리

여러 작업을 처리하도록 예약한 뒤에, 작업이 끝나면 결과를 받는 방식. 실행한 순서대로 진행되는 게 아니라 각자의 우선순위에 따라 일시정지하고 다른 coroutine을 돌린다.

## asyncio

### 이터러블, 이터레이터, 제너레이터

[image](https://nvie.com/img/relationships.png)

- 제너레이터 기반의 코루틴과 async def로 만든 코루틴을 구분하는 이유.

제너레이터 기반의 코루틴 링크 : https://techblog-history-younghunjo1.tistory.com/301


### 파이썬에서 코루틴의 종류

1. def, yield/yield from을 함께 사용하는 제너레이터 기반 코루틴
2. async와 await 키워드를 사용하는 Native 코루틴

