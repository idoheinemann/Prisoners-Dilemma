from itertools import combinations
import signal
from contextlib import contextmanager

import dilemma_lib
import prisoners


def raise_timeout():
    raise TimeoutError("runtime limit exceeded")


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def run_competition(turns_per_match=100, max_bot_runtime=1):
    from prisoners import LOYAL, BETRAY
    scores = {}
    for i in dilemma_lib.registered_classes:
        scores[i.__name__] = 0
    for cls1, cls2 in combinations(dilemma_lib.registered_classes, 2):
        print(f'{cls1.__name__} VS {cls2.__name__}')
        try:
            p1 = cls1()
        except BaseException as e:
            print(f'trying to create instance of {cls1.__name__} caused {e}')
            continue
        try:
            p2 = cls2()
        except BaseException as e:
            print(f'trying to create instance of {cls2.__name__} caused {e}')
            continue
        h1, h2 = [], []
        for i in range(turns_per_match):
            try:
                with timeout(max_bot_runtime):
                    c1 = p1.do_turn(h1)
            except BaseException as e:
                print(f'{cls1.__name__} crushed')
                print(e)
                break
            try:
                with timeout(max_bot_runtime):
                    c2 = p2.do_turn(h2)
            except BaseException as e:
                print(f'{cls2.__name__} crushed')
                print(e)
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
    return scores


def show_scores(scores: dict):
    name_score_tuples = list(scores.items())
    name_score_tuples.sort(key=lambda x: x[1], reverse=True)
    try:
        print(f'FIRST PLACE: {name_score_tuples[0][0]}')
        print(f'SECOND PLACE: {name_score_tuples[1][0]}')
        print(f'THIRD PLACE: {name_score_tuples[2][0]}')
    except:
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
