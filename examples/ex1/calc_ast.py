#!/usr/bin/env python

import sys
from os.path import dirname, realpath

# Add the funcparserlib_talk directory to the path to import recordtype
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from recordtype import recordtype


# AST nodes
Calculation = recordtype('Calculation', 'left, operator, right')
Operator = recordtype('Operator', 'sign')
Number = recordtype('Number', 'value')
