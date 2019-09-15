from itertools import combinations
import signal
from contextlib import contextmanager

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


if __name__ == '__main__':
    import prisoners
    from prisoners import LOYAL, BETRAY
    scores = {}
    for i in prisoners.registered_classes:
        scores[i.__name__] = 0
    for cls1, cls2 in combinations(prisoners.registered_classes, 2):
        p1, p2 = cls1(), cls2()
        h1, h2 = [], []
        for i in range(100):
            try:
                c1 = p1.do_turn(h1)
            except BaseException as e:
                print(f'{cls1.__name__} crushed')
                print(e)
                break
            try:
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

