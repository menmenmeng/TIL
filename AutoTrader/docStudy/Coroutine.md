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



### 파이썬에서 코루틴의 종류

1. def, yield/yield from을 함께 사용하는 제너레이터 기반 코루틴
2. async와 await 키워드를 사용하는 Native 코루틴


## 이터러블, 이터레이터, 제너레이터 (제너레이터가 그래서 뭐냐)

### iterator
파이썬 객체인데. 뭘 포함하고 있냐면, next 메소드를 포함하고 있다.
현재 상태를 알고 있을 때, 다음 상태가 어떤 값이 와야 하는지를 계산할 수 있는 객체 --> iterator.

- 이터레이터(iterator) : 값을 차례대로 꺼낼 수 있는 객체(object)
- for 반복문에서 "for i in range(100) :" 를 통해 0 ~ 99까지 연속된 숫자를 만들 때 사실 이터레이터 하나 생성 후 반복하여 숫자를 하나씩 꺼내면서 반복 처리
- 숫자가 많은 경우 메모리를 많이 사용하게 되어 성능 상 문제될 수 있음
- 이를 해결하기 위해 이터레이터만 생성하고 값이 필요한 시점에 값을 만드는 방식 사용 (지연 평가, lazy evaluation)

출처 https://skyfox83.tistory.com/120


### iterable
마찬가지로 객체인데 어떤 객체냐면, iterator를 반환할 수 있는 객체를 iterable이라고 한다.

next 함수를 계산할 수 있는 iterator를 내놓을 수 있는 객체.


### generator
iterator는 next를 계산하는 계산식을, 또는 로직을 따로 만들어 놓은 컨셉의 객체이다.

generator는 next를 계산하는 게 아니라. next를 내놔야 할 때 그때그때 다른 값을 내놓도록 함


~~~python
# ex. iterator
class MyIterator():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.num = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < self.end:
            res = self.num
            self.num += 1
            return res
        else:
            raise StopIteration

# ex. generator
def myGenerator(start, end):
    yield start
    while start < end:
        start += 1
        yield start
    return
~~~

둘 다 같은 역할을 함.

- iterator에서 next메서드의 역할 vs generator에서 yield의 역할
  - iterator에서 next : 다음 요소를 계산해주는 통합적인 계산식, 함수
  - generator에서 yield : 다음 요소를 반환해주는 역할은 똑같지만 다음 요소를 통합적으로 계산하는 수식이 있는 게 아니라. 제너레이터 안에서 yield를 만날 때마다 yield에 쓴 요소를 반환함.
    - __generator 안의 yield에서 함수를 사용하면 coroutine처럼 사용할 수 있음. 그래서 제너레이터 기반 coroutine이라고 하는 것__



![image](https://nvie.com/img/relationships.png){:.lead loading="lazy"}

- 제너레이터 기반의 코루틴과 async def로 만든 코루틴을 구분하는 이유.

제너레이터 기반의 코루틴 링크 : https://techblog-history-younghunjo1.tistory.com/301




## 동기 / 비동기 프로그래밍

### 동기 처리

특정 작업이 끝나면 다음 작업을 처리하는 __순차 처리 방식__

### 비동기 처리

여러 작업을 처리하도록 예약한 뒤에, 작업이 끝나면 결과를 받는 방식. 실행한 순서대로 진행되는 게 아니라 각자의 우선순위에 따라 일시정지하고 다른 coroutine을 돌린다.

## asyncio

### asyncio의 두 가지 많이 쓰이는(것 같은) 메소드

1. async def main()
2. await

async def main() : 비동기 프로그래밍 작성의 기본이다. async def를 통해 구현된 함수는 코루틴이라고 부른다.

async함수는 await에서 suspend되고, await대상의 값이 준비되면 resume되어 실행을 이어나간다.

코루틴 함수 : async def 함수.

코루틴 객체 : 코루틴 함수를 호출하여 반환된 객체.


asyncio.run(main())을 통해 main 코루틴 객체를 실행할 수 있다. asyncio.run()은 항상 새로운 이벤트 루프를 만들고, 코루틴을 실행한 뒤 끝에 이벤트 루프를 닫는다.

여기서 중요한 점, jupyter는 시작할 때부터 이미 디폴트의 이벤트 루프를 가지고 있다. 이벤트 루프는 꼭 한 번에 하나만 돌아갈 수 있고, 그래서 우리는 jupyter상에서는 run()을 하면 오류가 나게 됨.

jupyter가 이미 event loop 를 돌리고 있으므로, 우리가 만든 async def main() 의 main() 함수를 돌리려면 await main()을 하면 된다. (

await을 만나면 loop은 await 대상의 값이 준비될 때까지 suspend되고, 그 다음에 값이 준비 되면 resume된다.


await 뒤에 쓰일 수 있는 객체를 awaitable 객체라고 함. awaitable 객체에는 코루틴(async로 선언된 함수), 태스크, 퓨처가 있다.

코루틴의 생성과 실행.... 코루틴이 생성되는 건 async로 선언된 함수를 실행하기만 하면 되는 것 같음. 이런 경우 코루틴이 생성되지만, 함수가 실행되지는 않는다..

태스크는 asyncio.create_task() 함수로 감싸서, 코루틴이 실행되도록 예약된다. 그리고 task 객체를 반환. 코루틴이 동시에 실행되도록 예약할 때 사용된다...

코루틴을 그냥 실행하는 것과, 태스크로 만들어서 실행하는 것의 차이를 보여주는 두 가지 예시.

#### 코루틴 실행

~~~python
import asyncio, time
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
async def main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
~~~

await이 say_after()의 값이 나올 때까지 기다린다(1초) ->
await이 say_after()의 값이 나올 때까지 기다린다(2초)

합 3초 동안 main이 돌아감.


#### 태스크 실행

~~~python
import asyncio, time
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
~~~

await이 task1의 값이 나올 때까지 기다린다 (task1은 say_after라는 코루틴을 돌리기로 예약된 상태 자체를 반환함.)
반환되었으니,

await이 다시 task2의 값이 나올 때까지 기다린다.

create_task로 만들어지는 태스크는 비동기 작업 객체이다. 따라서, 두 개의 코루틴을 동시에 돌리고 싶다면 create_task를 통해 task로 만들어준 뒤에 활용해야 함.


궁금한 점... 어쨌든 노트북의 프로세서는 하나만 있지 않나. 프로세서가 하나뿐인데 파이썬 위에서 비동기 객체를 만들어서 돌린다고 해서 이게 동시에 돌아갈 수가 있는 거야?

노트북의 프로세서가 몇 개인가. 16개인데 어떻게 24개, 30개 이상이 계속해서 돌아갈 수 있는 건지는 모르겠음.

아무튼, 비동기 프로그래밍이 가능함. task를 활용해서, 실시간 트레이더를 만들 수 있을 것 같다.
