school = {"1반" : [172, 185, 198, 177, 165, 199], "2반" : [165, 177, 167, 180, 191]}
try:
    for class_number, students in school.items():
        for student in students:
            if student > 190:
                print(f'{class_number}에 190을 넘는 학생이 있습니다.')
                # 여기서 전부 끝내기 위해서, break를 쓰면 두 번째 for문에서는 나가기를 못하게 될 거다!!
                # 중첩된 for문을 바로 종료하고 싶을 땐 error를 발생시켜 본다.
                raise StopIteration
except StopIteration:
    print('정상종료')