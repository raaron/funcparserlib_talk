#!/usr/bin/env python

import unittest
from pyml_parser import PymlParser
from pyml_ast import *


class PymlParserTest(unittest.TestCase):

    # Input for parsing with a variable test_attribute to check your solutions
    pyml = """
MainWindow {
    test_attribute = %s;

    Label {
        Image {
            path = "a.png";
        }
    }

    Button {
        text = "OK";
        width = 60;
    }
}
"""

    # How the corresponding AST should look like after parsing:
    ast_should = Widget('MainWindow', [None], [
        Widget('Label', [], [
            Widget('Image', [Attribute('path', 'a.png')], [])
        ]),
        Widget('Button', [Attribute('text', 'OK'), Attribute('width', 60)], [])
    ])

    def setUp(self):
        self.parser = PymlParser()

    def test_basic(self):
        """Check if parsing pyml works."""

        self.check_test_attribute("4", 4)

    def test_calculation_value(self):
        """
        Check if parsing an attribute having a calculation as value works.
        This test fails until you add support for calculation attribute values.
        """
        should_value = Calculation(Number(1), Operator('+'), Number(2))
        self.check_test_attribute("1 + 2", should_value)

    def test_string_list_value(self):
        """
        Check if parsing an attribute having a list of strings as value works.
        This test fails until you add support for stringlist attribute values.
        """
        self.check_test_attribute('["red", "green"]', ["red", "green"])

    def check_test_attribute(self, input_value, should_value):
        """
        Helper for parsing and checking pyml. Takes the pyml
        input_value: string in pyml syntax for test_attribute's value
        should_value: how the corresponding node should look like in the AST
        """
        ast_is = self.parser.parse(self.pyml % input_value)
        self.ast_should.attributes[0] = Attribute('test_attribute', should_value)
        self.assertEqual(ast_is, self.ast_should)


if __name__ == '__main__':
    unittest.main()
