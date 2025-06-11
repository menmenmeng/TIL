"""
문제
크기가 N(1 ≤ N ≤ 100,000)인 1차원 배열 A[1], …, A[N]이 있다. 어떤 i, j(1 ≤ i ≤ j ≤ N)에 대한 점수는, (A[i] + … + A[j]) × min{A[i], …, A[j]}가 된다. 즉, i부터 j까지의 합에 i부터 j까지의 최솟값을 곱한 것이 점수가 된다.

배열이 주어졌을 때, 최대의 점수를 갖는 부분배열을 골라내는 프로그램을 작성하시오.

입력
첫째 줄에 정수 N이 주어진다. 다음 줄에는 A[1], …, A[N]을 나타내는 정수들이 주어진다. 각각의 정수들은 음이 아닌 값을 가지며, 1,000,000을 넘지 않는다.

출력
첫째 줄에 최대 점수를 출력한다.
"""
N = int(input())
L = list(map(int, input().split()))

def func(source):
    n = len(source)
    
    # base case
    if n == 1:
        return source[0]**2
    
    # divide and conquer
    l1, l2 = source[:n//2], source[n//2:]
    max1, max2 = func(l1), func(l2)
    
    # logic
    start, end = n//2 - 1, n//2
    height = min(source[start], source[end])
    summ = source[start] + source[end]
    value = height * summ
    while True:
        if start == 0 and end == n-1:
            break
        elif start == 0 and end != n-1:
            end += 1
            height = min(height, source[end])
            summ += source[end]
        elif start != 0 and end == n-1:
            start -= 1
            height = min(height, source[start])
            summ += source[start]
        elif source[start-1] > source[end+1]:
            start -= 1
            height = min(height, source[start])
            summ += source[start]
        elif source[start-1] <= source[end+1]:
            end += 1
            height = min(height, source[end])        
            summ += source[end]

        if value < height * summ:
            value = height * summ
    return max(max1, max2, value)

print(func(L))