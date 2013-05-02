#!/usr/bin/env python

from Tkinter import *

from text_change_visitor import TextChangeVisitor
from politeness_visitor import PolitenessVisitor
from enlarge_visitor import EnlargeVisitor
from gui_visitor import GuiVisitor
from pyml_ast import get_test_ast


def execute_visitors(ast, visitors):
    """
    Executes 'visitors' in the given order on the 'ast'.
    Returns the return value of the final visitor.
    """
    result = None
    for visitor in visitors:
        result = visitor().visit(ast)
    return result


if __name__ == '__main__':
    ast = get_test_ast()
    visitors = (TextChangeVisitor, PolitenessVisitor, EnlargeVisitor, GuiVisitor)
    mainwindow = execute_visitors(ast, visitors)
    print ast.repr()
    mainwindow.mainloop()
