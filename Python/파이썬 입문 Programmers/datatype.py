s = "Hello world"
print(type(s))
print(type(s)==str)
i = 1
print(type(i))
print(type(i)==int)
d = 3.513
print(type(d))
print(type(d)==float)

import numpy as np
i = 1
print(type(i))
print(type(i)==np.int8) # 이건 False가 나옴

print(isinstance(1, int))
print(isinstance(42.90, float))


