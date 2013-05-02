#!/usr/bin/env python

from pyml_ast import get_test_ast
import base_visitor


class EnlargeVisitor(base_visitor.BaseVisitor):
    """Increases width and height of MainWindows and Frames by 100."""

    def visit_mainwindow(self, mainwindow):
        self.enlarge(mainwindow)
        self.visit_children(mainwindow)

    def visit_frame(self, frame):
        self.enlarge(frame)
        self.visit_children(frame)

    def enlarge(self, widget):
        """Increase width and height of 'widget' by 100."""
        widget.width += 100
        widget.height += 100



if __name__ == '__main__':
    ast = get_test_ast()
    v = EnlargeVisitor()
    v.visit(ast)
    print ast.repr()
