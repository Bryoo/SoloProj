class Person(object):
    def __init__(self):
        pass


class Fellow(Person):
    def __init__(self, name):
        self.name = name
        self.id = id(self)


class Staff(Person):
    def __init__(self, name):
        self.name = name
        self.id = id(self)
