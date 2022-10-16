from datetime import datetime
import math

# def f22i(numFloat): # float to double ints
#     if numFloat%1==0:
#         return numFloat, numFloat
#         # if res[0] == res[1], use this result.(calculation :  "returnFunction(f) = return")
#     else:
#         x = (numFloat-math.ceil(numFloat))/(math.floor(numFloat)-math.ceil(numFloat))
#         return math.floor(numFloat), math.ceil(numFloat), round(x, 7), round(1-x, 7) # round를 꼭 써야 하는지에 대해 생각해보기.
#         # if res[0] != res[1], use this result.(calculation : "returnFunction(res[0]) * res[2] + returnFunction(res[1]) * res[3] = return")

def ms2dt(ms):
    return datetime.fromtimestamp(ms/1000)

def dt2ms(*dt):
    try:
        res = int(round(datetime.timestamp(datetime(*dt))*1000, -3))
    except:
        res = int(round(datetime.timestamp(*dt)*1000, -3))
    return res

