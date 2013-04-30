#!/usr/bin/env python

from pyml_ast import get_test_ast
import base_visitor


class EnlargeVisitor(base_visitor.BaseVisitor):
    """Increases width and height of MainWindows and Frames by 100."""

    def visit_mainwindow(self, mainwindow):
        # TODO: Increase the size of the mainwindow
        pass

    def visit_frame(self, frame):
        # TODO: Increase the size of the frame
        pass


if __name__ == '__main__':
    ast = get_test_ast()
    v = EnlargeVisitor()
    v.visit(ast)
    print ast.repr()
