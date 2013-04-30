#!/usr/bin/env python

from pyml_ast import get_test_ast
import base_visitor


class TextChangeVisitor(base_visitor.BaseVisitor):
    """Adds a prefix to all Button and Label texts."""

    def visit_button(self, button):
        button.text = "BUTTON: " + button.text

    def visit_label(self, label):
        label.text = "LABEL: " + label.text


if __name__ == '__main__':
    ast = get_test_ast()
    v = TextChangeVisitor()
    v.visit(ast)
    print ast.repr()
