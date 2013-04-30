#!/usr/bin/env python

from pyml_ast import MainWindow, Frame, Button, Label


class BaseVisitor(object):
    """Adds a prefix to all Buttons and Labels."""

    def visit(self, ast, *args):
        """
        Call the visiting method for this Ast node.
        For some visitors, passing arguments from node to node is useful,
        use 'arg' for this purpose.
        """

        mapping = {MainWindow: self.visit_mainwindow,
                   Frame: self.visit_frame,
                   Button: self.visit_button,
                   Label: self.visit_label}

        return mapping[ast.__class__](ast, *args)

    def visit_children(self, ast, *args):
        """Visit all children of the 'ast'."""

        for child in ast.children:
            self.visit(child, *args)

    def visit_mainwindow(self, mainwindow, *args):
        self.visit_children(mainwindow, *args)

    def visit_frame(self, frame, *args):
        self.visit_children(frame, *args)

    def visit_button(self, button, *args):
        pass

    def visit_label(self, label, *args):
        pass
