from dilema_lib import *


class BetrayPrisoner(Prisoner):
    def do_turn(self, history: list):
        return BETRAY


class LoyalPrisoner(Prisoner):
    def do_turn(self, history: list):
        return LOYAL


class TitForTatPrisoner(Prisoner):
    def do_turn(self, history: list):
        if len(history) == 0:
            return LOYAL
        return history[-1][0]


class RandomPrisoner(Prisoner):
    def __init__(self):
        import random
        self.random = random.Random()

    def do_turn(self, history: list):
        return self.random.choice([BETRAY, LOYAL])
