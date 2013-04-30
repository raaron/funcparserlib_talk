#!/usr/bin/env python

import unittest
from calc_parser import CalculationParser
from calc_ast import *


class CalculationParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = CalculationParser()

    def test_addition(self):
        """Check if parsing an addition works."""

        ast_is = self.parser.parse("1 + 2")
        ast_should = Calculation(Number(1), Operator('+'), Number(2))
        self.assertEqual(ast_is, ast_should)

    def test_subtraction(self):
        """
        Check if parsing a subtraction works.
        This test fails until you add support for subtraction.
        """
        ast_is = self.parser.parse("1 - 2")
        ast_should = Calculation(Number(1), Operator('-'), Number(2))
        self.assertEqual(ast_is, ast_should)


if __name__ == '__main__':
    unittest.main()
