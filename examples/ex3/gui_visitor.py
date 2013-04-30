#!/usr/bin/env python

from Tkinter import *

from pyml_ast import get_test_ast
import base_visitor


class GuiVisitor(base_visitor.BaseVisitor):
    """Replaces 'shit' by peeep in any visible text."""

    def visit_mainwindow(self, mainwindow):
        widget = Tk()
        widget.title(mainwindow.title)
        widget.geometry("%dx%d" % (mainwindow.width, mainwindow.height))
        self.visit_children(mainwindow, widget)
        return widget

    def visit_frame(self, frame, parent=None):
        widget = Frame(parent, borderwidth=1, relief=SUNKEN,
                       height=frame.height, width=frame.width)

        # Keep the frames size even if widgets are added
        widget.pack_propagate(0)

        self.visit_children(frame, widget)
        return self.pack(widget)

    def visit_button(self, button, parent=None):
        widget = Button(parent, text=button.text)
        return self.pack(widget)

    def visit_label(self, label, parent=None):
        widget = Label(parent, text=label.text)
        return self.pack(widget)

    def pack(self, widget):
        """
        Pack 'widget' with default padding and anchor.
        Returns the widget.
        """
        widget.pack(padx=5, pady=5, anchor=W)
        return widget


if __name__ == '__main__':
    ast = get_test_ast()
    v = GuiVisitor()
    mainwindow = v.visit(ast)
    print ast.repr()
    mainwindow.mainloop()
