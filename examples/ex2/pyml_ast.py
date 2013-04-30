#!/usr/bin/env python

import sys
from os.path import dirname, realpath

# Add the funcparserlib_talk directory to the path to import recordtype
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from recordtype import recordtype


def attribute_repr(self, indent_level=0):
    """Pretty print for an attribute."""

    indent = '\t' * indent_level
    return '%s{Attribute: %s = %s}' % (indent, self.key, str(self.value))


def widget_repr(self, indent_level=0):
    """Pretty print for a widget."""

    indent = '\t' * indent_level
    attrs = '\n'.join([a.repr(indent_level + 1) for a in self.attributes])
    child_widgets = '\n\n'.join([c.repr(indent_level + 1) for c in self.child_widgets])
    if attrs and child_widgets:
        attrs += '\n\n'
    return '%s{Widget: %s\n%s%s\n%s}' % (indent, self.name, attrs, child_widgets, indent)


# AST nodes

# TODO: Make your changes here ################################################

Attribute = recordtype('Attribute', 'key, value')
Widget = recordtype('Widget', 'name, attributes, child_widgets')

# Give them a pretty print method
Attribute.repr = attribute_repr
Widget.repr = widget_repr
