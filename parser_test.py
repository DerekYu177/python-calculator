import unittest
import pytest

from . import parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    # basic tests

    def test_simple_addition(self):
        assert 2 == self.parser("1+1")

    def test_simple_addition_with_space(self):
        assert 2 == self.parser("1 + 1")

    def test_double_digit_addition(self):
        assert 48 == self.parser("24 + 24")

    def test_simple_subtraction(self):
        assert 3 == self.parser("5 - 2")

    def test_double_digit_subtraction(self):
        assert -12 == self.parser("24 - 36")

    def test_simple_multiplication(self):
        assert 6 == self.parser("2 * 3")

    def test_simple_division(self):
        assert 4 == self.parser("16 / 4")

    # exception tests

    def test_divide_by_zero_raise_error(self):
        with pytest.raises(ZeroDivisionError):
            self.parser("100 / 0")

    def test_unbalanced_brackets_returns_exception(self):
        with pytest.raises(parser.UnbalancedExpressionError):
            self.parser("((( 1+1 ")

    # moderate complexity tests

    def test_multiple_additions(self):
        # assert 5 == self.parser("1+1+1+1+1")
        pass

    def test_simple_brackets(self):
        assert 2 == self.parser("(1+1)")

    def test_double_brackets(self):
        assert 2 == self.parser("((1+1))")

    def test_bracket_in_simple(self):
        assert 3 == self.parser("1 + (1 + 1)")
