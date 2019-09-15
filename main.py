from itertools import combinations
import signal
from contextlib import contextmanager
import sys

import dilemma_lib
from prisoners import BETRAY, LOYAL


def raise_timeout(x1, x2):
    raise TimeoutError("time limit passed")


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def get_disable_prints():
    stdout, stderr = sys.stdout, sys.stderr

    class __T:
        def __enter__(self):
            sys.stdout, sys.stderr = None, None

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout, sys.stderr = stdout, stderr

    return __T()


disable_prints = get_disable_prints()


def run_competition(bots=None, turns_per_match=100, max_bot_runtime=1):
    scores = {}
    if bots is None:
        bots = dilemma_lib.registered_classes
    for i in bots:
        scores[i.__name__] = 0
    for cls1, cls2 in combinations(bots, 2):
        print(f'{cls1.__name__} VS {cls2.__name__}')
        try:
            with disable_prints:
                p1 = cls1()
        except BaseException as e:
            print(f'trying to create instance of {cls1.__name__} caused {e}')
            continue
        try:
            with disable_prints:
                p2 = cls2()
        except BaseException as e:
            print(f'trying to create instance of {cls2.__name__} caused {e}')
            continue
        h1, h2 = [], []
        for i in range(turns_per_match):
            try:
                with timeout(max_bot_runtime):
                    with disable_prints:
                        c1 = p1.do_turn(h1)
            except BaseException as e:
                print(f'{cls1.__name__} crushed: {e}')
                break
            try:
                with timeout(max_bot_runtime):
                    with disable_prints:
                        c2 = p2.do_turn(h2)
            except BaseException as e:
                print(f'{cls2.__name__} crushed: {e}')
                break
            if c1 is LOYAL and c2 is LOYAL:
                scores[cls1.__name__] += 5
                scores[cls2.__name__] += 5
            elif c1 is LOYAL and c2 is BETRAY:
                scores[cls1.__name__] += 0
                scores[cls2.__name__] += 20
            elif c1 is BETRAY and c2 is LOYAL:
                scores[cls1.__name__] += 20
                scores[cls2.__name__] += 0
            elif c1 is BETRAY and c2 is BETRAY:
                scores[cls1.__name__] += 1
                scores[cls2.__name__] += 1
            else:
                if c1 not in {BETRAY, LOYAL}:
                    print(f'{cls1.__name__} returned illegal output: {c1}')
                else:
                    print(f'{cls2.__name__} returned illegal output: {c2}')
            h1.append((c1, c2))
            h2.append((c2, c1))
    return scores


def show_scores(scores: dict):
    name_score_tuples = list(scores.items())
    name_score_tuples.sort(key=lambda x: x[1], reverse=True)
    try:
        winners = name_score_tuples.copy()
        for place in ['FIRST', 'SECOND', 'THIRD']:
            print(f'{place} PLACE: {" & ".join(x[0] for x in winners if x[1] == winners[0][1])}')
            if place == 'THIRD':
                break
            winners = [x for x in winners if x[1] != winners[0][1]]
            if len(winners) == 0:
                break
    except IndexError:
        pass
    print()
    for index, (name, score) in enumerate(name_score_tuples):
        print(f'{index + 1}. {name} => {score}')


if __name__ == '__main__':
    print('finished registering competitors')
    print()
    print()
    print('running competition...')
    results = run_competition()
    print()
    print()
    print('finished running competitions')
    print('calculating results...')
    print()
    show_scores(results)
