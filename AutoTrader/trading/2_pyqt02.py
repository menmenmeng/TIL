import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
# 이 위가, 기본 코드다.