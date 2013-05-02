#!/usr/bin/env python

from base_visitor import BaseVisitor
import operator


class EvaluatorVisitor(BaseVisitor):
    """Evaluates a Javali program."""

    def __init__(self):
        super(EvaluatorVisitor, self).__init__()
        self.variables = None
        self.result = []

    def evaluate(self, program):
        """Main entry point to evaluate a program by calling Main.main()."""

        self.variables = {}
        self.result = []
        return self.visit(program)

    def visit_binary_expression(self, binary_expr):
        """Evaluates a binary expression."""

        operators = {'+': operator.add,
                     '-': operator.sub,
                     '*': operator.mul,
                     '/': operator.div,
                     '<': operator.lt,
                     '<=': operator.le,
                     '>': operator.gt,
                     '>=': operator.ge,
                     '==': operator.eq,
                     '!=': operator.ne}

        left = self.visit(binary_expr.left)
        right = self.visit(binary_expr.right)
        op = operators[binary_expr.op]
        return op(left, right)

    def visit_int_const(self, int_const):
        """Return the value of the IntConst."""

        if int_const.sign == '-':
            return -int_const.value
        else:
            return int_const.value

    def visit_variable(self, variable):
        """Return the current value of this variable."""

        return self.variables[variable.name]

    def visit_assignment(self, assignment):
        """
        Update the LHS of the assignment with the evaluated value of the RHS.
        """
        self.variables[assignment.variable.name] = self.visit(assignment.expr)

    def visit_put_call(self, put_call):
        """
        Print the evaluated value of the expression in parentheses.
        """
        self.result.append(self.visit(put_call.expr))

    def visit_while_statement(self, while_stmt):
        """
        Executes the 'body' of the while loop as long as 'condition'
        evaluates to True.
        """
        condition = self.visit(while_stmt.condition)
        while condition:
            self.visit_all(while_stmt.body)
            condition = self.visit(while_stmt.condition)

    def visit_if_statement(self, if_stmt):
        """
        Executes the 'if_body' if 'condition' evaluates to True, otherwise
        'else_body' is evaluated if there is an else branch.
        """
        condition = self.visit(if_stmt.condition)
        if condition:
            self.visit_all(if_stmt.if_body)
        elif if_stmt.else_body:
            self.visit_all(if_stmt.else_body)
