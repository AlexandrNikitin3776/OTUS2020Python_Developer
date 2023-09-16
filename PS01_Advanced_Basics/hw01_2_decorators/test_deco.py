from deco import foo, bar, fib
import unittest


class TestDecorators(unittest.TestCase):
    def test_foo(self):
        print(foo(4, 3))
        print(foo(4, 3, 2))
        print(foo(4, 3))
        print("foo was called", foo.calls, "times")
        self.assertEqual(foo.calls, 2)

    def test_bar(self):
        print(bar(4, 3))
        print(bar(4, 3, 2))
        print(bar(4, 3, 2, 1))
        print("bar was called", bar.calls, "times")
        self.assertEqual(bar.calls, 3)

    def test_fib(self):
        print(fib.__doc__)
        fib(4)
        print(fib.calls, "calls made")
        self.assertEqual(fib.calls, 7)
