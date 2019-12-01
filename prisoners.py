from dilemma_lib import Prisoner, BETRAY, LOYAL


class LoyalPrisoner(Prisoner):
    def do_turn(self, history: list):
        return LOYAL


class BetrayPrisoner(Prisoner):
    def do_turn(self, history: list):
        return BETRAY


class TitForTatPrisoner(Prisoner):
    def do_turn(self, history: list):
        if len(history) == 0:
            return LOYAL
        return history[-1][1]


class BetrayEveryOtherTurnPrisoner(Prisoner):
    def do_turn(self, history: list):
        if len(history) % 2 == 0:
            return LOYAL
        return BETRAY


class RandomPrisoner(Prisoner):
    def __init__(self):
        import random
        self.__random = random

    def do_turn(self, history: list):
        return self.__random.choice([BETRAY, LOYAL])


class DoWhatOtherDidMostPrisoner(Prisoner):
    def do_turn(self, history: list):
        what_other_did = {LOYAL: 0, BETRAY: 0}
        for i in history:
            what_other_did[i[1]] += 1
        if what_other_did[LOYAL] >= what_other_did[BETRAY]:
            return LOYAL
        return BETRAY
