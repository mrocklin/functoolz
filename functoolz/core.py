from functools import reduce

def identity(x):
    return x


def remove(predicate, coll):
    """ Return those items of collection for which predicate(item) is true.

    >>> from functoolz import remove
    >>> def even(x):
    ...     return x % 2 == 0
    >>> list(remove(even, [1, 2, 3, 4]))
    [1, 3]
    """
    return filter(lambda x: not predicate(x), coll)


def thread_first(val, *forms):
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_first(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the first input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_first(1, (add, 4), (pow, 2))  # pow(add(4, 1), 2)
    25

    So in general
        thread_first(x, f, (g, y, z))
    expands to
        g(f(x), y, z)

    See Also:
        thread_last
    """
    def evalform_front(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            fn, args = form[0], form[1:]
            args = (val,) + args
            return fn(*args)
    return reduce(evalform_front, forms, val)


def thread_last(val, *forms):
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_last(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the last input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_last(1, (add, 4), (pow, 2))  # pow(2, add(1, 4))
    32

    So in general
        thread_last(x, f, (g, y, z))
    expands to
        g(y, z, f(x))

    >>> def even(x): return x % 2 == 0
    >>> list(thread_last([1, 2, 3], (map, inc), (filter, even)))
    [2, 4]

    See Also:
        thread_first
    """
    def evalform_back(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            fn, args = form[0], form[1:]
            args = args + (val,)
            return fn(*args)
    return reduce(evalform_back, forms, val)


def hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False


import collections
def memoize(f, cache=None):
    """ Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed
        Only use on pure functions

    >>> def add(x, y):  return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y
    """
    if cache == None:
        cache = {}
    def memof(*args):
        if not hashable(args):
            return f(*args)
        elif args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result
    memof.__name__ = f.__name__
    memof.__doc__ = f.__doc__
    return memof
