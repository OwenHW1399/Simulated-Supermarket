"""CSC148 Assignment 1: Tests for Customer

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the Customer class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import Customer
from store import Item


def test_complete_init() -> None:
    customer = Customer("Empty", [])
    assert customer.arrival_time == -1
    assert customer.name == "Empty"
    assert customer.num_items() == 0
    assert customer.get_item_time() == 0


def test_complete() -> None:
    customer = Customer("test1", [Item('apple\\34', 34), Item('apple\\43', 43), Item('apple\\567', 567),
                                  Item('apple\\785', 785)])
    assert customer.arrival_time == -1
    assert customer.name == "test1"
    for item in customer._items:
        lst = item.name.split('\\')
        assert lst[0].isalpha()
        assert lst[1].isnumeric()
        assert item.get_time() == int(lst[1])
    assert customer.num_items() == 4
    assert customer.get_item_time() == 77 + 567 + 785


if __name__ == '__main__':
    import pytest

    pytest.main(['test_customer.py'])
