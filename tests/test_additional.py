import pytest

from app.calculator import add, multiply


def test_add_positive():
    assert add(3, 4) == 7


def test_multiply_by_zero():
    assert multiply(5, 0) == 0
