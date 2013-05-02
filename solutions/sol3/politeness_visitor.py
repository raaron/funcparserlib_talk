#!/usr/bin/env python

from pyml_ast import get_test_ast
import base_visitor


class PolitenessVisitor(base_visitor.BaseVisitor):
    """Replaces 'shit' by 'peeep' in any visible text."""

    def visit_mainwindow(self, mainwindow):
        mainwindow.title = self.get_polite(mainwindow.title)
        self.visit_children(mainwindow)

    def visit_button(self, button):
        button.text = self.get_polite(button.text)

    def visit_label(self, label):
        label.text = self.get_polite(label.text)



    def get_polite(self, txt):
        """
        Returns txt with every occurence of 'shit' being replaced by 'peeep'.
        """
        return txt.replace('shit', 'peeep')


if __name__ == '__main__':
    ast = get_test_ast()
    v = PolitenessVisitor()
    v.visit(ast)
    print ast.repr()
