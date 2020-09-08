"""CSC148 Assignment 1: Tests for GroceryStore

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the GroceryStore class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from store import GroceryStore, Customer, Item
from store import EXPRESS_LIMIT

# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.

CONFIG_FILE_111_03 = '''{
  "regular_count": 1,
  "express_count":1,
  "self_serve_count": 1,
  "line_capacity": 3
}
'''
CONFIG_FILE_000_00 = '''{
  "regular_count": 0,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 0
}
'''
CONFIG_FILE_010_01 = '''{
  "regular_count": 0,
  "express_count": 1,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''
CONFIG_FILE_100_03 = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 3
}
'''
CONFIG_FILE_111_02 = '''{
  "regular_count": 1,
  "express_count": 1,
  "self_serve_count": 1,
  "line_capacity": 2
}
'''


def test_enter_line():
    f = StringIO(CONFIG_FILE_000_00)
    store1 = GroceryStore(f)
    customer = Customer('Chris', [Item('bread', 3)])
    assert store1.enter_line(customer) == -1
    f.close()
    f = StringIO(CONFIG_FILE_010_01)
    store2 = GroceryStore(f)
    lst = []
    for i in range(EXPRESS_LIMIT + 2):
        item = Item('pan', 2)
        lst.append(item)
    customer1 = Customer("Owen", lst)
    assert store2.enter_line(customer1) == -1


def test_enter_line2():
    f = StringIO(CONFIG_FILE_111_02)
    store3 = GroceryStore(f)
    lst3 = []
    for i in range(EXPRESS_LIMIT + 2):
        item = Item('pan', 2)
        lst3.append(item)
    customer3 = Customer('a', lst3)
    customer4 = Customer('b', [Item('a', 2)])
    customer5 = Customer('c', [Item('a', 20)])
    customer6 = Customer('d', [Item('a', 2)])
    customer9 = Customer('g', [Item('a', 2)])
    lst10 = []
    for i in range(EXPRESS_LIMIT + 2):
        item = Item('pan', 2)
        lst10.append(item)
    customer10 = Customer('h', lst10)
    assert store3.enter_line(customer4) == 0
    assert store3.enter_line(customer3) == 2
    assert store3.enter_line(customer5) == 1
    assert store3.enter_line(customer6) == 0
    assert store3.enter_line(customer10) == 2
    assert store3.enter_line(customer9) == 1


def test_start_and_complete_check_out():
    f = StringIO(CONFIG_FILE_111_02)
    store3 = GroceryStore(f)
    lst = []
    for i in range(EXPRESS_LIMIT + 3):
        item = Item('pan', 2)
        lst.append(item)
    customer3 = Customer('a', lst)
    customer4 = Customer('b', [Item('a', 2)])
    customer5 = Customer('c', [Item('a', 20)])
    customer6 = Customer('d', [Item('a', 2)])
    customer9 = Customer('g', [Item('a', 2)])
    lst10 = []
    for i in range(EXPRESS_LIMIT + 2):
        item = Item('pan', 2)
        lst10.append(item)
    customer10 = Customer('h', lst10)
    store3.enter_line(customer4)
    store3.enter_line(customer3)
    store3.enter_line(customer5)
    store3.enter_line(customer6)
    store3.enter_line(customer10)
    store3.enter_line(customer9)
    assert store3.start_checkout(0) == 2
    assert store3.complete_checkout(0)
    assert store3.start_checkout(0) == 2
    assert not store3.complete_checkout(0)
    assert store3.start_checkout(1) == 20
    assert store3.complete_checkout(1)
    assert store3.start_checkout(1) == 2
    assert not store3.complete_checkout(1)
    assert store3.start_checkout(2) == 40
    assert store3.complete_checkout(2)
    assert store3.start_checkout(2) == 36
    assert not store3.complete_checkout(2)
    assert store3.start_checkout(0) == 0
    assert store3.start_checkout(1) == 0
    assert store3.start_checkout(2) == 0


def test_line_is_ready_and_close():
    f = StringIO(CONFIG_FILE_100_03)
    store4 = GroceryStore(f)
    customer1 = Customer('b', [Item('a', 29)])
    customer2 = Customer('c', [Item('a', 2)])
    customer3 = Customer('d', [Item('a', 2)])
    store4.enter_line(customer1)
    assert store4.line_is_ready(0)
    store4.enter_line(customer2)
    store4.enter_line(customer3)
    assert len(store4.close_line(0)) == 2
    assert store4.line_is_ready(0)
    assert store4.start_checkout(0) == 29
    assert not store4.complete_checkout(0)
    assert not store4.line_is_ready(0)


def test_get_first_in_line():
    f = StringIO(CONFIG_FILE_100_03)
    store4 = GroceryStore(f)
    customer1 = Customer('b', [Item('a', 29)])
    customer2 = Customer('c', [Item('a', 2)])
    store4.enter_line(customer1)
    store4.enter_line(customer2)
    assert store4.get_first_in_line(0) == customer1
    assert store4.complete_checkout(0)
    assert store4.get_first_in_line(0) == customer2
    assert not store4.complete_checkout(0)
    assert store4.get_first_in_line(0) is None


if __name__ == '__main__':
    import pytest

    pytest.main(['test_grocerystore.py'])
