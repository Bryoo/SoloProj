
class Room(object):
    max = 0
    pass

class Office(Room):
    def __init__(self, name):
        self.name = name


class LivingSpace(Room):
    def __init__(self, name):
        self.name = name
    pass
