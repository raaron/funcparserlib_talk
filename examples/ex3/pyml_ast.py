#!/usr/bin/env python

import sys
from os.path import dirname, realpath

# Add the funcparserlib_talk directory to the path to import recordtype
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from recordtype import recordtype


def pyml_repr(self, indent_level=0):
    """Pretty print for any pyml element."""

    indent = '\t' * indent_level
    class_name = self.__class__.__name__
    attrs = '\n'.join(['%s\t%s = %s' % (indent, k, v) for k, v in self.todict().iteritems() if k != 'children'])

    if hasattr(self, 'children'):
        children = '\n\n'.join([c.repr(indent_level + 1) for c in self.children])
        if attrs and children:
            attrs += '\n\n'
        return '%s{%s:\n%s%s\n%s}' % (indent, class_name, attrs, children, indent)
    else:
        return '%s{%s:\n%s\n%s}' % (indent, class_name, attrs, indent)


def get_test_ast():
    """Returns a pyml ast for testing."""

    m = MainWindow('some title', 200, 150, [
            Frame(180, 80, [
                Label('some text'),
                Button('shit'),
            ]),
            Label('shit happens')
        ])
    return m


# Define AST possible nodes
MainWindow = recordtype('MainWindow', 'title, width, height, children')
Frame = recordtype('Frame', 'width, height, children')
Button = recordtype('Button', 'text')
Label = recordtype('Label', 'text')

# Give them a pretty print method
for cls in [MainWindow, Frame, Button, Label]:
    cls.repr = pyml_repr