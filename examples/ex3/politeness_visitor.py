#!/usr/bin/env python

from pyml_ast import get_test_ast
import base_visitor


class PolitenessVisitor(base_visitor.BaseVisitor):
    """Replaces 'shit' by 'peeep' in any visible text."""

    def visit_mainwindow(self, mainwindow):
        # TODO: check the window title
        pass

    def visit_button(self, button):
        # TODO: check the button text
        pass

    def visit_label(self, label):
        # TODO: check the label text
        pass


if __name__ == '__main__':
    ast = get_test_ast()
    v = PolitenessVisitor()
    v.visit(ast)
    print ast.repr()
