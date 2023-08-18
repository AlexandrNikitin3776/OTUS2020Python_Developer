from deco import foo, bar, fib


def test_foo():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")
    assert foo.calls == 2


def test_bar():
    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")
    assert bar.calls == 3


def test_fib():
    print(fib.__doc__)
    fib(4)
    print(fib.calls, "calls made")
    assert fib.calls == 7
