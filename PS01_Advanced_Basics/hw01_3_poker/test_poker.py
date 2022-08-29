import unittest

from poker import best_hand, best_wild_hand, card_ranks, flush, kind, straight, two_pair


class TestRanks(unittest.TestCase):
    def test_card_rank(self):
        hand = "2C 3C 4C 5C 6C 7C 8C 9C TC JC QC KC AC"
        ranks = card_ranks(hand.split())
        self.assertEqual(ranks, [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2])


class TestFlush(unittest.TestCase):
    def test_flush(self):
        test_cases = [
            {
                "hand": "2C",
                "expected": True,
            },
            {
                "hand": "2C 3C",
                "expected": True,
            },
            {
                "hand": "2C 3S",
                "expected": False,
            },
        ]
        for tc in test_cases:
            with self.subTest(tc):
                result = flush(tc["hand"].split())
                self.assertEqual(result, tc["expected"])


class TestStraight(unittest.TestCase):
    def test_straight(self):
        test_cases = [
            {
                "ranks": [2],
                "expected": True,
            },
            {
                "ranks": [3, 2],
                "expected": True,
            },
            {
                "ranks": [2, 3],
                "expected": False,
            },
            {
                "ranks": [5, 3, 2],
                "expected": False,
            },
        ]
        for tc in test_cases:
            with self.subTest(tc):
                result = straight(tc["ranks"])
                self.assertEqual(result, tc["expected"])


class TestKind(unittest.TestCase):
    def test_kind(self):
        test_cases = [
            {
                "n": 2,
                "ranks": [2, 2],
                "expected": 2,
            },
            {
                "n": 2,
                "ranks": [],
                "expected": None,
            },
            {
                "n": 2,
                "ranks": [6, 5, 5, 3, 3],
                "expected": 5,
            },
        ]
        for tc in test_cases:
            with self.subTest(tc):
                result = kind(tc["n"], tc["ranks"])
                self.assertEqual(result, tc["expected"])


class TestTwoPair(unittest.TestCase):
    def test_two_pair(self):
        test_cases = [
            {
                "ranks": [2],
                "expected": None,
            },
            {
                "ranks": [2, 2, 2, 2],
                "expected": [2, 2],
            },
            {
                "ranks": [3, 3, 2, 2],
                "expected": [3, 2],
            },
        ]
        for tc in test_cases:
            with self.subTest(tc):
                result = two_pair(tc["ranks"])
                self.assertEqual(result, tc["expected"])


class TestPokerHands(unittest.TestCase):
    def test_hand(self):
        test_cases = [
            {
                "hand": "6C 7C 8C 9C TC 5C JS",
                "expected": ["6C", "7C", "8C", "9C", "TC"],
            },
            {
                "hand": "TD TC TH 7C 7D 8C 8S",
                "expected": ["8C", "8S", "TC", "TD", "TH"],
            },
            {
                "hand": "JD TC TH 7C 7D 7S 7H",
                "expected": ["7C", "7D", "7H", "7S", "JD"],
            },
        ]

        for tc in test_cases:
            with self.subTest(tc):
                result = best_hand(tc["hand"].split())
                self.assertEqual(set(result), set(tc["expected"]))

    def test_best_wild_hand(self):
        test_cases = [
            {
                "hand": "6C 7C 8C 9C TC 5C ?B",
                "expected": ["7C", "8C", "9C", "JC", "TC"],
            },
            {
                "hand": "TD TC 5H 5C 7C ?R ?B",
                "expected": ["7C", "TC", "TD", "TH", "TS"],
            },
            {
                "hand": "JD TC TH 7C 7D 7S 7H",
                "expected": ["7C", "7D", "7H", "7S", "JD"],
            },
        ]
        for tc in test_cases:
            with self.subTest(tc):
                result = best_wild_hand(tc["hand"].split())
                self.assertEqual(set(result), set(tc["expected"]))
