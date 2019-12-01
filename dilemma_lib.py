import abc
from typing import NewType


def _():  # make the registered classes variable invisible
    __registered_classes = []

    def _register(cls):
        if hasattr(cls, 'do_turn'):
            print(f'registering {cls.__name__}...')
            __registered_classes.append(cls)
        else:
            print(f'class {cls.__name__} does not have a method do_turn')

    def _get_registered_classes():
        return __registered_classes

    return _register, _get_registered_classes


register, get_registered_classes = _()


class PrisonerAction:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return str(self)

LOYAL = PrisonerAction('LOYAL')
BETRAY = PrisonerAction('BETRAY')


class Prisoner(abc.ABC):
    """
    prisoner base class
    all prisoner bots must inherit from the prisoner class

    Note! constructor for this class cannot accept any arguments
    Note! printing will not work when using do_turn
    """

    def __init_subclass__(cls, **kwargs):
        register(cls)

    @abc.abstractmethod
    def do_turn(self, history: list) -> PrisonerAction:
        """
        runs a single turn and return's the prisoners choice

        :param history: a list of all the history so fur, each event is consisted of two elements, the first is your
            action that turn, and the second is your opponent's action.

        :type history: list[tuple[int, int]]

        :return: the action for this turn, either LOYAL or BETRAY
        """
