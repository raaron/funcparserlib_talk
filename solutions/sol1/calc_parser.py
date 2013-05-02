#!/usr/bin/env python

import sys
from os.path import dirname, realpath

from calc_ast import Number, Operator, Calculation

# Add the funcparserlib_talk directory to the path to import some helpers
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from funcparserlib_helpers import number, op, unarg, end, tokenize


class CalculationParser(object):
    """Parser for input of the form 'NUMBER + NUMBER'."""

    def __init__(self):
        nr = number >> Number

        # TODO: Make your changes in this section #############################

        additive_operator = (op('+') | op('-')) >> Operator
        calculation = nr + additive_operator + nr >> unarg(Calculation)

        #######################################################################

        self.toplevel = calculation + end

    def parse(self, txt):
        """Parses the 'txt' and returns an AST."""
        return self.toplevel.parse(tokenize(txt))


if __name__ == '__main__':
    p = CalculationParser()
    ast = p.parse('1 - 2')
    print ast
