#!/usr/bin/env python

import unittest
from interpreter import Interpreter

BASIC_CODE = """
a = 1
b = 2
c = a + b

while (c < 5) {
  c = c + 1
  put(c)

  while (a < 3) {
    a = a + 1
    put(a)
  }
}

put(3 + 5 * 2)
put(3 < 5)
"""

BASIC_RESULT_SHOULD = [4, 2, 3, 5, 13, True]

COMPARISON_OPERATORS_CODE = """
put(0 < 1)
put(1 < 0)
put(0 > 1)
put(1 > 0)
put(0 == 1)
put(0 == 0)
put(0 <= 1)
put(1 <= 0)
put(0 <= 0)
put(0 >= 1)
put(1 >= 0)
put(0 >= 0)
put(0 != 1)
put(0 != 0)
"""

COMPARISON_RESULT_SHOULD = [True, False, False, True, False, True, True, False,
                            True, False, True, True, True, False]

NEGATIVE_INTEGERS_CODE = """
put(-2)
put(1 + -2)
"""

NEGATIVES_RESULT_SHOULD = [-2, -1]

IF_STMT_CODE = """
if (1 < 2) {
    if (3 < 4) {
        put(3)
    }
} else {
    if (5 < 6) {
        put(5)
    }
}
"""

IF_STMT_RESULT_SHOULD = [3]


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_basic(self):
        """Check if interpreting with the initial version works."""

        self.check_result(BASIC_CODE, BASIC_RESULT_SHOULD)

    def test_comparison_operators(self):
        """
        Check if the following comparison operators work:
            - <
            - >
            - ==
            - <=
            - >=
            - !=

        This test fails until you add support for this operators in the
        parser and the evaluator.
        """
        self.check_result(COMPARISON_OPERATORS_CODE, COMPARISON_RESULT_SHOULD)

    def test_negative_integers(self):
        """
        Check if code containing negative integers work., e.g. '1 + -2'
        This test fails until you add support for negative integers in the
        parser, javali_ast and the evaluator.
        """
        self.check_result(NEGATIVE_INTEGERS_CODE, NEGATIVES_RESULT_SHOULD)

    def test_if_stmt(self):
        """
        Check if if statements of the following form work:

        if (1 < 2) {
            put(1)
        } else {
            put(2)
        }

        The else block is optional:

        if (1 < 2) {
            put(1)
        }

        This test fails until you add support for if-statements in the
        parser, javali_ast and the evaluator.
        """
        self.check_result(IF_STMT_CODE, IF_STMT_RESULT_SHOULD)

    def check_result(self, code, result_should):
        """
        Helper for interpreting javali 'code' and comparing the result of the
        interpreter to 'result_should'.
        """
        self.interpreter.interprete_code(code)
        self.assertEqual(self.interpreter.get_result(), result_should)


if __name__ == '__main__':
    unittest.main()
