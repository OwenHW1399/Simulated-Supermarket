"""CSC148 Assignment 1: Tests for checkout classes

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the checkout classes.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import RegularLine, ExpressLine, SelfServeLine
from store import Item, Customer
from store import EXPRESS_LIMIT


# Checkoutline(0)? test

def test_regular_init() -> None:
    line = RegularLine(3)
    assert len(line) == 0
    assert len(line.queue) == 0
    assert line.is_open is True
    assert len(line.queue) == 0


def test_regular_empty_line() -> None:
    line = RegularLine(3)
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0


def test_regular_empty_line_close() -> None:
    line = RegularLine(3)
    initial_state = line.is_open
    lst = line.close()
    assert len(lst) == 0
    assert initial_state is True
    assert line.is_open is False


def test_regular_customer_coming_test() -> None:
    line = RegularLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c3 = Customer("Jon", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c4 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c5 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    for item in [c1, c2, c3, c4, c5]:
        assert line.can_accept(item)
    line.close()
    for item in [c1, c2, c3, c4, c5]:
        assert not line.can_accept(item)


def test_regular_customer_joining_test() -> None:
    line = RegularLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c3 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c4 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    counter = 1
    for item in [c1, c2, c3, c4]:
        if counter in (1, 2, 3):
            assert line.can_accept(item)
            assert line.accept(item)
        else:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1
    assert counter == 5
    assert len(line) == 3
    assert c1 in line.queue
    assert c2 in line.queue
    assert c3 in line.queue
    assert c4 not in line.queue
    assert line.queue[0] is c1
    assert line.queue[1] is c2
    assert line.queue[2] is c3


def test_regular_start_checkout_test() -> None:
    line = RegularLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 5)])
    c3 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 33)])
    c4 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 23)])
    for item in [c1, c2, c3, c4]:
        if line.can_accept(item):
            line.accept(item)
    assert line.start_checkout() == 6
    assert len(line) == 3
    assert line.start_checkout() == 6
    assert line.complete_checkout() is True
    assert line.start_checkout() == 8
    assert line.complete_checkout() is True
    assert line.start_checkout() == 36
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0
    assert line.complete_checkout() is False


def test_regular_close_test() -> None:
    line = RegularLine(4)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 3), Item("lid", 1), Item("fan", 3)])
    c5 = Customer("James", [Item("milk", 32), Item("lid", 1), Item("fan", 3)])
    c6 = Customer("Janice", [Item("milk", 42), Item("lid", 1), Item("fan", 3)])
    counter = 1
    for item in [c1, c2, c5, c6]:
        if counter <= 3:
            assert line.can_accept(item)
            assert line.accept(item)
        if counter == 3:
            assert len(line.queue) == 3
            assert line.queue[0] is c1
            assert line.queue[1] is c2
            assert line.queue[2] is c5
            assert line.close() == [c2, c5]
            assert c1 in line.queue
            assert len(line.queue) == 1
            assert line.queue[0] == c1
        if counter > 3:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1


# This below is express line:
def test_express_init_() -> None:
    line = ExpressLine(3)
    assert len(line) == 0
    assert line.is_open == True
    assert len(line.queue) == 0


def test_express_empty_line() -> None:
    line = ExpressLine(3)
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0


def test_express_customer_coming_test() -> None:
    line = ExpressLine(3)
    lst = []
    for i in range(EXPRESS_LIMIT + 1):
        lst.append(Item("lid", 1))
    c1 = Customer("Jameson", lst)
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c3 = Customer("Jon", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c4 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c5 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    counter = 1
    for item in [c1, c2, c3, c4, c5]:
        if counter == 1:
            assert not line.can_accept(item)
        elif item.num_items() <= EXPRESS_LIMIT:
            assert line.can_accept(item)
        else:
            assert not line.can_accept(item)
        counter += 1

    line.close()
    for item in [c1, c2, c3, c4, c5]:
        assert not line.can_accept(item)


def test_express_joining_in_extreme() -> None:
    line = ExpressLine(3)
    lst = []
    lst2 = []
    lst3 = []
    for i in range(EXPRESS_LIMIT + 1):
        lst.append(Item("lid", 1))
    for i in range(EXPRESS_LIMIT + 1):
        lst2.append(Item("Item_2" + str(i), 1))
    for i in range(EXPRESS_LIMIT + 1):
        lst3.append(Item("Item_3" + str(i), 1))

    c1 = Customer("Jon", lst2)
    c2 = Customer("James", lst3)
    c3 = Customer("Janice", lst)
    for item in [c1, c2, c3]:
        assert not line.can_accept(item)
        assert not line.accept(item)

    assert len(line) == 0
    assert line.capacity == 3
    assert c1 not in line.queue
    assert c2 not in line.queue
    assert c3 not in line.queue


def test_express_customer_joining_test() -> None:
    line = ExpressLine(3)
    lst = []
    lst2 = []
    lst3 = []
    for i in range(EXPRESS_LIMIT + 1):
        lst.append(Item("lid", 1))
    for i in range(EXPRESS_LIMIT):
        lst2.append(Item("Item_2" + str(i), 1))
    for i in range(EXPRESS_LIMIT):
        lst3.append(Item("Item_3" + str(i), 1))

    c1 = Customer("Jon", lst2)
    c2 = Customer("James", lst3)
    c3 = Customer("Janice", lst)
    counter = 1
    for item in [c1, c2, c3]:
        if counter in (1, 2):
            assert line.can_accept(item)
            assert line.accept(item)
        else:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1
    assert counter == 4
    assert len(line) == 2
    assert line.capacity == 3
    assert c1 in line.queue
    assert c2 in line.queue
    assert c3 not in line.queue
    assert line.queue[0] is c1
    assert line.queue[1] is c2


def test_express_start_checkout_test() -> None:
    line = ExpressLine(3)
    lst = []
    lst2 = []
    lst3 = []
    for i in range(EXPRESS_LIMIT + 1):
        lst.append(Item("lid", 1))
    for i in range(EXPRESS_LIMIT - 1):
        lst2.append(Item("Item_2" + str(i), 1))
    for i in range(EXPRESS_LIMIT):
        lst3.append(Item("Item_3" + str(i), 2))

    c1 = Customer("Jon", lst2)
    c2 = Customer("James", lst3)
    c3 = Customer("Janice", lst)
    counter = 1
    for item in [c1, c2, c3]:
        if counter in (1, 2):
            assert line.can_accept(item)
            assert line.accept(item)
        else:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1
    assert len(line.queue) == 2
    assert line.capacity == 3
    assert line.queue[0] is c1
    assert line.queue[1] is c2
    assert line.start_checkout() == EXPRESS_LIMIT - 1
    assert len(line) == 2
    assert line.start_checkout() == EXPRESS_LIMIT - 1
    assert line.complete_checkout() is True
    assert line.start_checkout() == 2 * EXPRESS_LIMIT
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0
    assert len(line) == 0
    assert len(line.queue) == 0
    assert line.complete_checkout() is False


def test_express_normal_test_for_close_test() -> None:
    line = ExpressLine(2)
    lst = []
    lst2 = []
    lst3 = []
    for i in range(EXPRESS_LIMIT):
        lst.append(Item("lid", 10))
    for i in range(EXPRESS_LIMIT):
        lst2.append(Item("Item_2" + str(i), 1))
    for i in range(EXPRESS_LIMIT):
        lst3.append(Item("Item_3" + str(i), 2))

    c1 = Customer("Jon", lst2)
    c2 = Customer("James", lst3)
    c3 = Customer("Janice", lst)
    for item in [c1, c2, c3]:
        line.accept(item)
    assert len(line.queue) == line.capacity
    assert line.capacity == 2
    assert line.queue[0] is c1
    assert line.queue[1] is c2
    assert line.start_checkout() == EXPRESS_LIMIT
    assert line.complete_checkout() is True
    assert line.start_checkout() == EXPRESS_LIMIT * 2
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0
    assert len(line) == 0
    assert len(line.queue) == 0
    assert line.complete_checkout() is False


def test_express_close_test() -> None:
    line = ExpressLine(4)
    lst = []
    lst2 = []
    lst3 = []
    lst4 = []
    lst5 = []
    for i in range(EXPRESS_LIMIT):
        lst.append(Item("lid", 10))
    for i in range(EXPRESS_LIMIT):
        lst2.append(Item("Item_2" + str(i), 1))
    for i in range(EXPRESS_LIMIT):
        lst3.append(Item("Item_3" + str(i), 2))
    for i in range(EXPRESS_LIMIT):
        lst4.append(Item("lid", 100))
    counter = 1
    c1 = Customer("Jon", lst2)
    c2 = Customer("James", lst3)
    c3 = Customer("Janice", lst)
    c4 = Customer("Johnny", lst4)
    for item in [c1, c2, c3, c4]:
        if counter <= 3:
            assert line.can_accept(item)
            assert line.accept(item)
        if counter == 3:
            assert len(line.queue) == 3
            assert line.queue[0] is c1
            assert line.queue[1] is c2
            assert line.queue[2] is c3
            assert line.close() == [c2, c3]
            assert c1 in line.queue
            assert len(line.queue) == 1
            assert line.queue[0] == c1
        if counter > 3:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1


# self_serve
def test_self_init() -> None:
    line = SelfServeLine(3)
    assert len(line) == 0
    assert line.is_open is True
    assert len(line.queue) == 0


def test_self_empty_line() -> None:
    line = SelfServeLine(3)
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0


def test_self_empty_line_close() -> None:
    line = SelfServeLine(3)
    initial_state = line.is_open
    lst = line.close()
    assert len(lst) == 0
    assert initial_state is True
    assert line.is_open is False


def test_self_customer_coming_test() -> None:
    line = SelfServeLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c3 = Customer("Jon", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c4 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c5 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    for item in [c1, c2, c3, c4, c5]:
        assert line.can_accept(item)
    line.close()
    for item in [c1, c2, c3, c4, c5]:
        assert not line.can_accept(item)


def test_self_cutomer_joining_test() -> None:
    line = SelfServeLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c3 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c4 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    counter = 1
    for item in [c1, c2, c3, c4]:
        if counter in (1, 2, 3):
            assert line.can_accept(item)
            assert line.accept(item)
        else:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1
    assert counter == 5
    assert len(line) == 3
    assert c1 in line.queue
    assert c2 in line.queue
    assert c3 in line.queue
    assert c4 not in line.queue
    assert line.queue[0] is c1
    assert line.queue[1] is c2
    assert line.queue[2] is c3


def test_self_start_checkout_test() -> None:
    line = SelfServeLine(3)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 2), Item("lid", 1), Item("fan", 5)])
    c3 = Customer("James", [Item("milk", 2), Item("lid", 1), Item("fan", 33)])
    c4 = Customer("Janice", [Item("milk", 2), Item("lid", 1), Item("fan", 23)])
    for item in [c1, c2, c3, c4]:
        if line.can_accept(item):
            line.accept(item)
    assert line.start_checkout() == 12
    assert len(line) == 3
    assert line.start_checkout() == 12
    assert line.complete_checkout() is True
    assert line.start_checkout() == 16
    assert line.complete_checkout() is True
    assert line.start_checkout() == 72
    assert line.complete_checkout() is False
    assert line.start_checkout() == 0
    assert line.complete_checkout() is False


def test_self_close_test() -> None:
    line = SelfServeLine(4)
    c1 = Customer("John", [Item("milk", 2), Item("lid", 1), Item("fan", 3)])
    c2 = Customer("Jim", [Item("milk", 3), Item("lid", 1), Item("fan", 3)])
    c5 = Customer("James", [Item("milk", 32), Item("lid", 1), Item("fan", 3)])
    c6 = Customer("Janice", [Item("milk", 42), Item("lid", 1), Item("fan", 3)])
    counter = 1
    for item in [c1, c2, c5, c6]:
        if counter <= 3:
            assert line.can_accept(item)
            assert line.accept(item)
        if counter == 3:
            assert len(line.queue) == 3
            assert line.queue[0] is c1
            assert line.queue[1] is c2
            assert line.queue[2] is c5
            assert line.close() == [c2, c5]
            assert c1 in line.queue
            assert len(line.queue) == 1
            assert line.queue[0] == c1
        if counter > 3:
            assert not line.can_accept(item)
            assert not line.accept(item)
        counter += 1


if __name__ == '__main__':
    import pytest

    pytest.main(['test_checkouts.py'])
