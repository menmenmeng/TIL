sentence = "Hello world는 프로그래밍을 배우기에 아주 좋은 사이트 입니다."
word = "abcdef"

print(sentence.split())
print(word.split())
print(list(word))
strlist = str(list(word))
print(str(list(word)))

print(type(list(word)))
print(type(str(list(word))))
print(list(strlist))

ll = eval(str(list(word)))
print(ll)
print(type(ll))