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
    """
    metaclass for prisoner bot
    """
    def __new__(mcs, clsname, bases, attrs):
        newclass = super(MetaPrisoner, mcs).__new__(mcs, clsname, bases, attrs)
        register(newclass)  # here is your register function
        return newclass

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)


class Prisoner(metaclass=MetaPrisoner):
    """
    prisoner base class
    all prisoner bots must inherit from the prisoner class

    Note! constructor for this class cannot accept any arguments
    Note! printing will not work when using do_turn
    """

    def do_turn(self, history: list):
        """
        runs a single turn and return's the prisoners choice
        :param history: a list of all the history so fur, each event is consisted of two elements, the first is your
        action that turn, and the second is your opponent's action.
        :type history: list[tuple[int, int]]
        :return: the action for this turn, either LOYAL or BETRAY
        """
        raise NotImplementedError("Can't call abstract method Prisoner.do_turn")


LOYAL = 0
BETRAY = 1
