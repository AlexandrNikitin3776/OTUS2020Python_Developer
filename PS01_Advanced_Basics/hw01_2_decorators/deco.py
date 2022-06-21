from functools import update_wrapper

assigned = ("calls", "memo", "level")


def disable(func):
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


def decorator(func):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""

    def wrapper(*args, **kwargs):
        update_wrapper(wrapper, func, assigned=assigned)
        wrapper.calls += 1
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    wrapper.calls = 0
    return wrapper


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """

    def wrapper(*args):
        update_wrapper(wrapper, func, assigned=assigned)
        memo_value = wrapper.memo.get(str(args))
        if memo_value is not None:
            return memo_value
        result = func(*args)
        wrapper.memo[str(args)] = result
        return result

    update_wrapper(wrapper, func)
    wrapper.memo = {}
    return wrapper


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """

    def wrapper(*args):
        update_wrapper(wrapper, func, assigned=assigned)
        args = list(args)
        result = args.pop()
        while args:
            y = result
            x = args.pop()
            result = func(x, y)
        return result

    update_wrapper(wrapper, func)
    return wrapper


def trace(level_indent):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """

    def decorator_trace(func):
        input = "-->"
        output = "<--"

        def wrapper(*args):
            update_wrapper(wrapper, func, assigned=assigned)
            indent = wrapper.level * level_indent
            func_call_str = f"{func.__name__}({', '.join(map(str, args))})"
            print(indent, input, func_call_str)
            wrapper.level += 1
            result = func(*args)
            wrapper.level -= 1
            print(indent, output, func_call_str, "==", result)
            return result

        update_wrapper(wrapper, func)
        wrapper.level = 0
        return wrapper

    return decorator_trace


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(4)
    print(fib.calls, "calls made")


if __name__ == "__main__":
    main()
