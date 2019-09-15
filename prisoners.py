from dilema_lib import *


class BetrayPrisoner(Prisoner):
    def do_turn(self, history: list):
        return BETRAY


class LoyalPrisoner(Prisoner):
    def do_turn(self, history: list):
        return LOYAL


class DoWhatOtherDidBefore(Prisoner):
    def do_turn(self, history: list):
        if len(history) == 0:
            return LOYAL
        return history[-1][0]
