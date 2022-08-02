class Calculator():
    def __init__(self, x, y):
        self.x, self.y = x, y

    def add(self):
        return self.x + self.y

    def sub(self):
        return self.x - self.y

    def mul(self):
        return self.x * self.y

    def div(self):
        try:
            return self.x / self.y
        except ZeroDivisionError as e:
            print(e, 'occurred')
            return None