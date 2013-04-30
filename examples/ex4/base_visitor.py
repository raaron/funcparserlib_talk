#!/usr/bin/env python

import javali_ast
import re
import inspect


class BaseVisitor(object):
    """Abstract base class for an BaseVisitor."""

    def __init__(self):
        """
        Collect the Ast nodes that we should visit and create the mapping
        between all nodes and their visiting methods.
        """

        # Automatically collect Ast nodes from the ast module
        # Note: This only works as long as we want to visit all nodes defined
        #       in ast. Otherwise create the list explicitely:
        #       [Program, ClassDeclaration, ...]
        #       or remove a particular class from the auto-generated list.
        self.nodes_to_visit =  [cls[1] for cls in inspect.getmembers(javali_ast, inspect.isclass)]

        # Build the mapping between the Ast nodes and their visiting method.
        self.method_mapping = {node: self.__get_visit_method(node) for node in self.nodes_to_visit}

    def visit(self, ast, *args):
        """Call the visiting method for this Ast node."""

        return self.method_mapping[ast.__class__](ast, *args)

    def visit_all(self, asts, *args):
        """Call the visiting method for a sequence of Asts."""

        result = []
        for ast in asts:
            result.append(self.visit(ast, *args))

        return result

    def default_visit(self, ast, *args):
        """
        Default visiting method. Recursively visits all children of the ast.
        Note: Implement a custom visiting method (such as visit_program() below)
              if an ast node contains attributes to other asts twice or
              if it references its parent node.
        """
        for attr, value in ast.todict().iteritems():
            if isinstance(value, list):
                if value and value[0].__class__ in self.nodes_to_visit:
                    # The attribute holds a list of Ast nodes.
                    return self.visit_all(value, *args)

            elif value.__class__ in self.nodes_to_visit:
                # The attribute holds a single Ast node.
                return self.visit(value, *args)

    # def visit_program(self, program, *args):
    #     """
    #     Custom visiting method to visit a Program Ast node. The default_visit()
    #     method would visit the main class and main method twice.
    #     """
    #     self.visit_all(program.statements, *args)
    #     return program

    def __get_visit_method(self, node):
        """
        Try to find the visiting method for this node. If there is none
        defined, return the default_visit() method.
        """

        # Convert the class name of the node into snake case for the visiting method.
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', node.__name__)
        name = 'visit_%s' % re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        # Try to find a custom visiting method
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return self.default_visit
