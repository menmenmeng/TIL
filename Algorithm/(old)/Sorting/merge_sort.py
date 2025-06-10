def merge_sort(array):
    if len(array) == 1:
        return array
    
    else:
        mid = len(array)//2
        l1 = merge_sort(array[:mid])
        l2 = merge_sort(array[mid:])

        # merge
        res_array = []
        while True:
            try:
                if l1[0] < l2[0]:
                    res_array.append(l1[0])
                    l1.pop(0)
                else:
                    res_array.append(l2[0])
                    l2.pop(0)
            except:
                res_array = res_array + l1 + l2
                break

        return res_array
    

if __name__=="__main__":
    l = [5, 4, 3, 2, 66, 1]
    print(merge_sort(l))