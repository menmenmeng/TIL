source = list(map(int, input().split()))

def merge_sort(source):
    result = []
    n = len(source)
    
    # base case. 만약 list 길이가 1로, 더 나눠지지 못한다면 source 그 자체를 리턴
    if n == 1:
        return source
    
    # base case가 아닐 경우, divide
    l1, l2 = source[:n//2], source[n//2:]

    # conquer
    l1_sorted = merge_sort(l1)
    l2_sorted = merge_sort(l2)

    # 바로 아래 계층의 2개, divide-conquered 리스트가 어떻게 최종 합쳐지는지
    while l1_sorted and l2_sorted: # 둘 중 하나가 완전히 비지 않은 경우 while문이 지속 실행됨
        n1 = l1_sorted[0]
        n2 = l2_sorted[0]

        if n1 > n2:
            result.append(n2)
            l2_sorted = l2_sorted[1:]
        
        else:
            result.append(n1)
            l1_sorted = l1_sorted[1:]
    
    if l1_sorted:
        result.extend(l1_sorted)
    elif l2_sorted:
        result.extend(l2_sorted)

    return result


if __name__=="__main__":
    res = merge_sort(source) # merge_sort(list) 형태의 함수가 재귀호출되어야 한다.
    print(res)