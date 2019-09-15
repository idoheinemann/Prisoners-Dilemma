from dilemma_lib import Prisoner, BETRAY, LOYAL


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


class BadAssTitForTatPrisoner(Prisoner):
    def do_turn(self, history: list):
        if len(history) == 0:
            return BETRAY
        return history[-1][0]


class MaxOutPrisoner(Prisoner):
    def do_turn(self, history: list):
        d = {BETRAY: 0, LOYAL: 0}
        for _, choise in history:
            d[choise] += 1
        if d[BETRAY] > d[LOYAL]:
            return BETRAY
        return LOYAL


class BadAssMaxOutPrisoner(Prisoner):
    def do_turn(self, history: list):
        d = {BETRAY: 0, LOYAL: 0}
        for _, choise in history:
            d[choise] += 1
        if d[BETRAY] >= d[LOYAL]:
            return BETRAY
        return LOYAL


class GrudgePrisoner(Prisoner):
    def do_turn(self, history: list):
        if BETRAY in [x[1] for x in history]:
            return BETRAY
        return LOYAL
