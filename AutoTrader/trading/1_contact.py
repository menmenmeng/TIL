class Contact:
    def __init__(self, name, phone_number, e_mail, addr):
        self.name = name
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.addr = addr

    def print_info(self):
        print("Name:", self.name)
        print("Phone Number:", self.phone_number)
        print("E-mail:", self.e_mail)
        print("Address:", self.addr)

def set_contact():
    name = input("Name:")
    phone_number = input("Phone:")
    e_mail = input("E-mail:")
    addr = input("Address:")
    print(name, phone_number, e_mail, addr)

# 디버깅용 run 함수      
def run():
    set_contact()

# 실행되면. main으로 실행되면 run() 하고. 아니면 run() 하지 않는다.
if __name__=="__main__":
    run()