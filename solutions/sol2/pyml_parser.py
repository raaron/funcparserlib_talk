#!/usr/bin/env python

import sys
from os.path import dirname, realpath
from funcparserlib.parser import many, forward_decl

from pyml_ast import *

# Add the funcparserlib_talk directory to the path to import some helpers
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from funcparserlib_helpers import *


class PymlParser(object):
    """
    Parser for pyml, a UI modeling language for demonstration purpose.
    See the file 'input.pyml' for an example of pyml syntax.
    """

    def __init__(self):

        # TODO: Make your changes in this section #############################

        nr = number >> Number
        plus_operator = op('+') >> Operator
        calculation = nr + plus_operator + nr >> unarg(Calculation)

        string_list = inbrackets(listof(string))
        value = calculation | number | string | string_list

        #######################################################################

        attribute = rawname + op_("=") + value + semicolon >> unarg(Attribute)
        attributes = many(attribute)

        widgets = forward_decl()
        widget = rawname + opencurlyparen + attributes + widgets + closecurlyparen >> unarg(Widget)
        widgets.define(many(widget))

        self.toplevel = widget + end

    def parse(self, txt):
        """Parses the 'txt' and returns an AST."""
        return self.toplevel.parse(tokenize(txt))


if __name__ == '__main__':
    p = PymlParser()
    with open('input.pyml') as fobj:
        ast = p.parse(fobj.read())
    print ast.repr()
