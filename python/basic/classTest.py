class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.weight = 'weight'

    def walk(self):
        print("person is walking...")

    def talk(self):
        print("person is talking...")

    # public类型可以被子类、类内以及类外被访问。
    def publicfun(self):
        print("call public function")

    # 保护类型只能允许其本身与子类进行访问。
    def _protectedfun(self):
        print("call protected function")

    # private类型只能允许类内进行访问。
    def __privatefun(self):
        print("call private function")


class Chinese(Person):
    def __init__(self, name, age, language):  # 先继承，在重构
        super().__init__(name, age)
        self.language = language

    # 对父类的重写
    def walk(self):
        print(self.name + " is walking")

    # 对方法重载会覆盖之前的方法
    def walk(self, place):
        print(self.name + " is walking on " + place)


class American(Person):
    pass


# main仅当直接运行该程序会执行，其他程序调用不会执行
if __name__ == '__main__':
    c = Chinese('张三', 22, 'chinese')
    c.talk()
    c.walk('Beijing')
    # c.walk(),对方法重载会覆盖之前的方法导致执行报错

    c.publicfun()
    c._protectedfun()
    # c.__privatefun() private类型只能允许类内进行访问。
