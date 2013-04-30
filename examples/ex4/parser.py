#!/usr/bin/env python

import sys
from os.path import dirname, realpath
from funcparserlib.parser import many, forward_decl

from javali_ast import *

# Add the funcparserlib_talk directory to the path to import some helpers
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from funcparserlib_helpers import *


class Parser(object):

    def __init__(self):
        self.toplevel = None

        makeop = lambda s: op(s) >> const(lambda l, r: BinaryExpression(l, s, r))

        kw_while = kw('while')
        kw_put = kw('put')

        add = makeop('+')
        sub = makeop('-')
        mul = makeop('*')
        div = makeop('/')

        lt = makeop('<')

        equ = op_('=')

        int_const = number >> IntConst
        variable = rawname >> Variable

        atom = int_const | variable
        expr1 = atom + many((mul | div) + atom) >> eval_expr
        expr2 = expr1 + many((add | sub) + expr1) >> eval_expr
        comparison_expr = expr2 + many(lt + expr2) >> eval_expr

        put_call = kw_put + inparens(comparison_expr) >> PutCall
        assignment = variable + equ + expr2 >> unarg(Assignment)
        condition = openparen + comparison_expr + closeparen

        stmt_block = forward_decl()
        while_stmt = kw_while + condition + stmt_block >> unarg(WhileStatement)
        stmt = assignment | put_call | while_stmt
        stmt_block.define(opencurlyparen + many(stmt) + closecurlyparen)

        program = many(stmt) >> Program

        self.toplevel = program + end

    def parse(self, code):
        return self.toplevel.parse(tokenize(code))


if __name__ == '__main__':
    p = Parser()
    with open("input.javali", 'r') as f:
        program = p.parse(f.read())
    print program.repr()
