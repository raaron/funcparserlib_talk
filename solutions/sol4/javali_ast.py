#!/usr/bin/env python

import sys
from os.path import dirname, realpath

# Add the funcparserlib_talk directory to the path to import recordtype
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from recordtype import recordtype


def get_sequence_repr(stmts, indent_level=0):
    """Helper method to get a printable repr of a sequence of Ast nodes."""

    indent = '\t' * indent_level
    return ('\n%s' % indent).join([stmt.repr(indent_level) for stmt in stmts])


# Pretty print methods for all AST nodes:

def program_repr(self, indent_level=0):
    return """
{Program:
\t%s
}""" % (get_sequence_repr(self.statements, indent_level + 1))


def assignment_repr(self, indent_level=0):
    return '{Assignment: %s = %s}' % (self.variable.repr(), self.expr.repr())


def put_call_repr(self, indent_level=0):
    return '{PutCall: put(%s)}' % (self.expr.repr())


def while_stmt_repr(self, indent_level=0):
    indent = '\t' * indent_level
    body = get_sequence_repr(self.body, indent_level + 2)
    return """
%s{WhileStatement:
%s  while (%s) {
%s    %s
%s  }
%s}""" % (indent, indent, self.condition.repr(), indent, body, indent, indent)


def if_stmt_repr(self, indent_level=0):
    indent = '\t' * indent_level
    if_body = get_sequence_repr(self.if_body, indent_level + 2)
    result = """
%s{IfStatement:
%s  if (%s) {
%s    %s
%s  }""" % (indent, indent, self.condition.repr(), indent, if_body, indent)

    if self.else_body:
        print 'ELSE'
        else_body = get_sequence_repr(self.else_body, indent_level + 2)
        result += """ else {
%s    %s
%s  }
%s}""" % (indent, else_body, indent, indent)

    return result


def binary_expr_repr(self, indent_level=0):
    return '{Binary: %s %s %s}' % (self.left.repr(), str(self.op), self.right.repr())


def int_const_repr(self, indent_level=0):
    return '{IntConst: %s%s}' % (self.sign if self.sign else '', str(self.value))


def variable_repr(self, indent_level=0):
    return '{Variable: %s}' % self.name


# AST nodes:
Program = recordtype('Program', 'statements')
Assignment = recordtype('Assignment', 'variable, expr')
PutCall = recordtype('PutCall', 'expr')
WhileStatement = recordtype("WhileStatement", 'condition, body')
IfStatement = recordtype("IfStatement", 'condition, if_body, else_body')
BinaryExpression = recordtype('BinaryExpression', 'left, op, right')
IntConst = recordtype('IntConst', 'sign, value')
Variable = recordtype('Variable', 'name')


# Assign the pretty print functions to all nodes:
Program.repr = program_repr
Assignment.repr = assignment_repr
PutCall.repr = put_call_repr
WhileStatement.repr = while_stmt_repr
IfStatement.repr = if_stmt_repr
BinaryExpression.repr = binary_expr_repr
IntConst.repr = int_const_repr
Variable.repr = variable_repr
