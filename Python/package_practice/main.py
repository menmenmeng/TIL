import ex_package.ex_module01 as m1
from ex_package.ex_module02 import c, d, MyMul
from ex_package import ex_module03 as m3
import ex_package

print(m1.a, m1.b)
print(m1.MyAddition(3, 4))
    
print(c, d)
print(MyMul(c, d))

MyInst = m3.Calculator(5, 6)
print(MyInst.add(), MyInst.mul(), MyInst.sub(), MyInst.div())

print(ex_package.ex_module01.MyAddition(4, 5))