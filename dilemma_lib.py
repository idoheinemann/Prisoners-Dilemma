registered_classes = []


def register(cls):
    if not cls.__name__ == 'Prisoner':
        if hasattr(cls, 'do_turn'):
            if cls.do_turn != Prisoner.do_turn:
                print(f'registering {cls.__name__}...')
                registered_classes.append(cls)
            else:
                print(f'class {cls.__name__} does not override Prisoner.do_turn')
        else:
            print(f'class {cls.__name__} does not have a method do_turn')


class MetaPrisoner(type):
    def __new__(mcs, clsname, bases, attrs):
        newclass = super(MetaPrisoner, mcs).__new__(mcs, clsname, bases, attrs)
        register(newclass)  # here is your register function
        return newclass

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)


class Prisoner(metaclass=MetaPrisoner):
    def __init__(self):
        pass

    def do_turn(self, history: list):
        pass


LOYAL = 0
BETRAY = 1
