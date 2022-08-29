#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools

Ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return 8, max(ranks)
    elif kind(4, ranks):
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):
        return 5, ranks
    elif straight(ranks):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), ranks
    elif two_pair(ranks):
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), ranks
    else:
        return 0, ranks


def card_ranks(hand) -> list[int]:
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = [Ranks[card[0]] for card in hand]
    return sorted(ranks, reverse=True)


def flush(hand) -> bool:
    """Возвращает True, если все карты одной масти"""
    suits = [card[1] for card in hand]
    for suit in suits:
        if suit != suits[0]:
            return False
    return True


def straight(ranks) -> bool:
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    prev_rank = None
    for rank in ranks:
        if prev_rank is None:
            prev_rank = rank
            continue
        if prev_rank - rank != 1:
            return False
        prev_rank = rank
    return True


def kind(n, ranks) -> str | None:
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank
    return None


def two_pair(ranks) -> list[int] | None:
    """Если есть две пары, то возвращает два соответствующих ранга,
    иначе возвращает None"""
    pairs = []
    prev_rank = None
    for rank in ranks:
        if prev_rank is None:
            prev_rank = rank
            continue
        if prev_rank == rank:
            pairs.append(rank)
            prev_rank = None
            continue
        prev_rank = rank
    if len(pairs) >= 2:
        return pairs[:2]
    return


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт"""
    hand_combs = itertools.combinations([card for card in hand], 5)
    hand_ranks = [(hand_set, hand_rank(hand_set)) for hand_set in hand_combs]
    return max(hand_ranks, key=lambda x: x[1])[0]


def gen_hand(hand, color):
    ranks = "23456789TJQKA"
    if color == "black":
        suits = "CS"
    elif color == "red":
        suits = "HD"
    joker = [rank + suit for rank in ranks for suit in suits]
    for j in joker:
        yield hand + [j]


def gen_handj(hand):
    ranks = "23456789TJQKA"
    suits = "CS"
    jokerB = [rank + suit for rank in ranks for suit in suits]
    suits = "HD"
    jokerR = [rank + suit for rank in ranks for suit in suits]
    for jb in jokerB:
        for jr in jokerR:
            if jb not in hand and jr:
                yield hand + [jb] + [jr]


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    hand_ = hand[:]
    best_hand_list = []
    if "?B" in hand_ and "?R" in hand_:
        hand_.remove("?B")
        hand_.remove("?R")
        hand_gen = gen_handj(hand_)
    elif "?B" in hand_:
        hand_.remove("?B")
        hand_gen = gen_hand(hand_, "black")
    elif "?R" in hand_:
        hand_.remove("?R")
        hand_gen = gen_hand(hand_, "red")
    else:
        return best_hand(hand)

    for h in hand_gen:
        bh = best_hand(h)
        best_hand_list.append((bh, hand_rank(bh)))
    return max(best_hand_list, key=lambda x: x[1])[0]
