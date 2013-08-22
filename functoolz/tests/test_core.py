from functoolz.core import remove, thread_first, thread_last, memoize
from operator import add, mul

def even(x):           return x % 2 == 0
def odd(x):            return x % 2 == 1
def inc(x):            return x + 1
def double(x):         return 2*x

def test_remove():
    assert list(remove(even, range(5))) == list(filter(odd, range(5)))

def test_thread_first():
    assert thread_first(2) == 2
    assert thread_first(2, inc) == 3
    assert thread_first(2, inc, inc) == 4
    assert thread_first(2, double, inc) == 5
    assert thread_first(2, (add, 5), double) == 14

def test_thread_last():
    assert list(thread_last([1, 2, 3], (map, inc), (filter, even))) == [2, 4]

def test_memoize():
    fn_calls = [0]  # Storage for side effects

    def f(x, y):
        """ A docstring """
        fn_calls[0] += 1
        return x + y
    mf = memoize(f)

    assert mf(2, 3) == mf(2, 3)
    assert fn_calls == [1]  # function was only called once
    assert mf.__doc__ == f.__doc__
