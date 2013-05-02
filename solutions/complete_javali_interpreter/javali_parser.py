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

        kw_class = kw('class')
        kw_new = kw('new')
        kw_if = kw('if')
        kw_else = kw('else')
        kw_while = kw('while')
        kw_return = kw('return')

        add = makeop('+')
        sub = makeop('-')
        mul = makeop('*')
        div = makeop('/')

        equ = op_('=')

        int_const = number >> IntConst
        variable = rawname >> Variable
        type_ = rawname >> Type
        var_decl = type_ + rawname >> unarg(VarDeclaration)
        var_decls = many(var_decl + semicolon)

        method_call = forward_decl()
        atom = int_const | method_call | variable
        expr1 = atom + many((mul | div) + atom) >> eval_expr
        expr2 = expr1 + many((add | sub) + expr1) >> eval_expr
        method_call.define(rawname + inparens(maybe_empty_listof(expr2)) >> unarg(MethodCall))

        new_obj_expr = kw_new + type_ + openparen + closeparen >> NewObject
        assignment = variable + equ + (new_obj_expr | expr2) >> unarg(Assignment)
        return_stmt = kw_return + expr2 >> ReturnStatement
        simple_stmt = (assignment | method_call | return_stmt) + semicolon

        stmt_block = forward_decl()
        condition = openparen + expr2 + closeparen
        if_stmt = kw_if + condition + stmt_block + kw_else + stmt_block >> unarg(IfStatement)
        while_stmt = kw_while + condition + stmt_block >> unarg(WhileStatement)

        stmt = simple_stmt | if_stmt | while_stmt | return_stmt
        stmt_block.define(opencurlyparen + many(stmt) + closecurlyparen)

        method_decl = type_ + rawname + inparens(maybe_empty_listof(var_decl)) + \
                        opencurlyparen + var_decls + many(stmt) + \
                        closecurlyparen >> unarg(MethodDeclaration)

        method_decls = many(method_decl)
        class_decl = kw_class + rawname + opencurlyparen + var_decls + \
                      method_decls + closecurlyparen >> unarg(ClassDeclaration)

        program = many(class_decl) >> Program

        self.toplevel = program + end

    def parse(self, code):
        return self.toplevel.parse(tokenize(code))


if __name__ == '__main__':
    p = Parser()
    with open("input.javali", 'r') as f:
        program = p.parse(f.read())
    print program.repr()