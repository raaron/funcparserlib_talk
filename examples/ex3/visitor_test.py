#!/usr/bin/env python

import unittest
from Tkinter import Tk

from text_change_visitor import TextChangeVisitor
from politeness_visitor import PolitenessVisitor
from enlarge_visitor import EnlargeVisitor
from gui_visitor import GuiVisitor
from pyml_ast import get_test_ast
from coordinator import execute_visitors


class VisitorTest(unittest.TestCase):

    original_ast = get_test_ast()

    def setUp(self):

        # Get an ast we can visit with our visitors
        self.ast_to_visit = get_test_ast()

        # How should the visited ast look like (further modified by tests)?
        self.ast_should = get_test_ast()

        self.text_change_visitor = TextChangeVisitor()
        self.politeness_visitor = PolitenessVisitor()
        self.enlarge_visitor = EnlargeVisitor()
        self.gui_visitor = GuiVisitor()

    def test_text_change_visitor(self):
        """Check if the TextChangeVisitor works."""

        self.change_text_ast_should()
        self.text_change_visitor.visit(self.ast_to_visit)
        self.check_result()

    def test_gui_visitor(self):
        """Check if the GuiVisitor works."""

        mainwindow = self.gui_visitor.visit(self.ast_to_visit)
        self.assertTrue(isinstance(mainwindow, Tk))

        # Check that the original ast remained unchanged
        self.check_result()

    def test_politeness_visitor(self):
        """
        Check if the PolitenessVisitor works.
        This test fails until you have implemented the visitor properly.
        """
        self.polite_ast_should()
        self.politeness_visitor.visit(self.ast_to_visit)
        self.check_result()

    def test_enlarge_visitor(self):
        """
        Check if the EnlargeVisitor works.
        This test fails until you have implemented the visitor properly.
        """

        self.enlarge_ast_should()
        self.enlarge_visitor.visit(self.ast_to_visit)
        self.check_result()

    def test_coordinator(self):
        """
        Check if combining several visitors works.
        This test fails until you have implemented all visitors properly.
        """

        self.change_text_ast_should()
        self.polite_ast_should()
        self.enlarge_ast_should()

        visitors = (TextChangeVisitor, PolitenessVisitor,
                    EnlargeVisitor, GuiVisitor)

        mainwindow = execute_visitors(self.ast_to_visit, visitors)
        self.assertTrue(isinstance(mainwindow, Tk))
        self.check_result()

    def check_result(self):
        """Checks whether the visited ast looks how it should."""

        self.assertEqual(self.ast_to_visit, self.ast_should)

######################### Helpers to modify 'ast_should' ######################

    def enlarge_ast_should(self):
        """Enlarges 'ast_should' the way that EnlargeVisitor should do it too."""

        def enlarge(w):
            w.width = w.width + 100
            w.height = w.height + 100

        enlarge(self.ast_should)
        enlarge(self.ast_should.children[0])

    def change_text_ast_should(self):
        """
        Changes texts of 'ast_should' the way that TextChangeVisitor
        should do it too.
        """

        def add_prefix(w, prefix):
            w.text = prefix + w.text

        add_prefix(self.ast_should.children[0].children[0], "LABEL: ")
        add_prefix(self.ast_should.children[0].children[1], "BUTTON: ")
        add_prefix(self.ast_should.children[1], "LABEL: ")

    def polite_ast_should(self):
        """Polites 'ast_should' the way that PolitenessVisitor should do it too."""

        def get_polite(w):
            w.text = w.text.replace('shit', 'peeep')

        get_polite(self.ast_should.children[0].children[1])
        get_polite(self.ast_should.children[1])


if __name__ == '__main__':
    unittest.main()
