a = 1 or 10
b = 0 or 10

# 위의 경우, a는 1이 이미 True이므로, 뒤의 값을 계산하지 않고 a=1이 할당됨
# b는 0이 False이므로, 뒤의 값이 무조건 할당됨(뒤의 값이 True면 True, False면 False)
print('a=',a,'b=',b)

a = 1 and 10
b = 0 and 10

# 다음의 경우, a는 1이 True이므로 뒤의 것을 봐야 함, 뒤의 값이 무조건 할당됨. a = 10
# b의 경우 0에서 이미 False가 나왔으므로 뒤의 값은 계산하지 않음, b=0.

print('a=',a,'b=',b)