'''
<문제>
이 결과는 증명을 기념하기 위해 그의 다이어리에 “Eureka! num = Δ + Δ + Δ” 라고 적은것에서 유레카 이론으로 알려졌다. 꿍은 몇몇 자연수가 정확히 3개의 삼각수의 합으로 표현될 수 있는지 궁금해졌다. 위의 예시에서, 5와 10은 정확히 3개의 삼각수의 합으로 표현될 수 있지만 4와 6은 그렇지 않다.

자연수가 주어졌을 때, 그 정수가 정확히 3개의 삼각수의 합으로 표현될 수 있는지 없는지를 판단해주는 프로그램을 만들어라. 단, 3개의 삼각수가 모두 달라야 할 필요는 없다.

<시간제한>
1초

<예제>
입력
3
10
20
1000

출력
1
0
1


<해설>
k가 3부터 1000까지이므로, 3중 for문으로 시간초과 없이 완전탐색할 수 있다.
나는 각 target마다 3중 for문을 돌면서 삼각수 3개를 더해서 target이 될 수 있는지를 검사했는데,
정답지를 만든 사람은 아예 1001개의 list를 만들어서(index가 0부터 1000까지 있도록) 그 안에 1, 0으로 정답지를 만들어 넣었다.
내가 만든 것처럼 하면, k의 숫자가 많아지면 3중 for문 * k개 숫자의 시간복잡도가 드는 데 반해,
정답지에서는 k의 숫자가 많더라도 3중 for문 + k개 숫자 의 시간복잡도가 든다.
'''
# # 입력
# N = int(input())
# target_nums = []
# for _ in range(N):
#     target_nums.append(int(input()))

# # 1000 이하의 값을 가지는 삼각수 구하기
# i = 1
# tri_nums = []
# while i*(i+1)<2000:
#     tri_nums.append(int(i*(i+1)/2))
#     i += 1
# tri_num_size = len(tri_nums)

# breakFlag = 0
# for target in target_nums:
#     for i1 in range(tri_num_size):
#         for i2 in range(i1, tri_num_size):
#             for i3 in range(i2, tri_num_size):
#                 num1, num2, num3 = tri_nums[i1], tri_nums[i2], tri_nums[i3]
#                 if num1+num2+num3 == target:
#                     print(1)
#                     breakFlag = 1
#                     break
#             if breakFlag: break
#         if breakFlag: 
#             breakFlag = 0
#             break
#     else:
#         print(0)


# 정답 매우중요...
answer = [0] * 1001
triangleNum = []
for i in range(1, 45):
    triangleNum.append(i * (i + 1) // 2)

for one in triangleNum:
    for two in triangleNum:
        for three in triangleNum:
            if one + two + three <= 1000:
                answer[one + two + three] = 1

N = int(input())
for _ in range(N):
    target = int(input())
    print(answer[target])
