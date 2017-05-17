
class Room(object):

    pass

class Office(Room):
    max = 6

    def __init__(self, name):
        self.name = name


class LivingSpace(Room):
    max = 4

    def __init__(self, name):
        self.name = name
    pass
