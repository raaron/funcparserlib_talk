import sys
from os.path import dirname, realpath

# Add the funcparserlib_talk directory to the path to import recordtype
sys.path.insert(0, dirname(dirname(realpath(__file__))))
from recordtype import recordtype


def get_sequence_repr(stmts, indent_level=0):
    """Helper method to get a printable repr of a sequence of Ast nodes."""

    indent = '\t' * indent_level
    return ('\n%s' % indent).join([stmt.repr(indent_level) for stmt in stmts])


######################## More complicated Ast nodes: ##########################


class Program(object):
    """Ast node for a javali program."""

    def __init__(self, class_decls):
        """
        Try to find class Main and its method main() and build a mapping
        between all class names and their ClassDeclarations.
        """
        self.class_decls = class_decls

        self.main_class = None
        self.main_method = None

        for class_decl in self.class_decls:
            if class_decl.name == "Main":
                self.main_class = class_decl
                for method_decl in class_decl.method_decls:
                    if method_decl.name == "main":
                        self.main_method = method_decl

        self.class_mapping = {c.name: c for c in self.class_decls}

    def repr(self, indent_level=0):
        class_decls = get_sequence_repr(self.class_decls, indent_level + 1)
        return """
{Program:
  %s
}""" % (class_decls)







############ Simple Ast nodes, defined with recordtype.recordtype: ############


# Define custom __repr__ functions for all of them:


def class_decl_repr(self, indent_level=0):
    indent = '\t' * indent_level
    method_decls = get_sequence_repr(self.method_decls, indent_level + 2)
    return """
%s{ClassDeclaration:
%s  %s {
%s    %s
%s  }
%s}""" % (indent, indent, self.name, indent, method_decls, indent, indent)


def method_decl_repr(self, indent_level=0):
    indent = '\t' * indent_level
    stmts = get_sequence_repr(self.stmts, indent_level + 2)
    params = ', '.join([p.repr() for p in self.parameters])
    return """
%s{MethodDeclaration:
%s  %s %s(%s) {
%s    %s
%s  }
%s}""" % (indent, indent, self.return_type.repr(), self.name, params,
          indent, stmts, indent, indent)


def var_decl_repr(self, indent_level=0):
    return '{VarDeclaration: %s: %s}' % (self.type_.repr(), self.name)


def type_repr(self, indent_level=0):
    return '{Type: %s}' % self.name


def new_obj_repr(self, indent_level=0):
    return "{New Object: new %s()}" % self.type_.name


def assignment_repr(cls, indent_level=0):
    return '{Assignment: %s = %s}' % (cls.variable.repr(), cls.expr.repr())


def return_stmt_repr(cls, indent_level=0):
    return '{ReturnStatement: %s}' % (cls.expr.repr())


def method_call_repr(self, indent_level=0):
    pars = ", ".join([p.repr() for p in self.parameters])
    return '{MethodCall: %s(%s)}' % (self.name, pars)


def if_stmt_repr(self, indent_level=0):
    indent = '\t' * indent_level
    if_block = get_sequence_repr(self.if_block, indent_level + 2)
    else_block = get_sequence_repr(self.else_block, indent_level + 2)
    return """
%s{IfStatement:
%s  if (%s) {
%s    %s
%s  }
%s  else {
%s    %s
%s  }
%s}""" % (indent, indent, self.condition.repr(), indent, if_block, indent, indent,
          indent, else_block, indent, indent)


def while_stmt_repr(self, indent_level=0):
    indent = '\t' * indent_level
    body = get_sequence_repr(self.body, indent_level + 2)
    return """
%s{WhileStatement:
%s  while (%s) {
%s    %s
%s  }
%s}""" % (indent, indent, self.condition.repr(), indent, body, indent, indent)


def binary_expr_repr(self, indent_level=0):
    return '{Binary: %s %s %s}' % (self.left.repr(), str(self.op), self.right.repr())


def int_const_repr(self, indent_level=0):
    return '{IntConst: %s}' % (str(self.value))


def variable_repr(self, indent_level=0):
    return '{Variable: %s}' % self.name


# Define simple Ast nodes using recordtype.recordtype to keep the code short.

ClassDeclaration = recordtype('ClassDeclaration', 'name, fields, method_decls')
MethodDeclaration = recordtype('MethodDeclaration',
                        'return_type, name, parameters, local_decls, stmts')

VarDeclaration = recordtype('VarDeclaration', 'type_, name')
Type = recordtype('Type', 'name')
NewObject= recordtype('NewObject', 'type_')
Assignment = recordtype('Assignment', 'variable, expr')
ReturnStatement = recordtype('ReturnStatement', 'expr')
MethodCall = recordtype('MethodCall', 'name, parameters')
IfStatement = recordtype("IfStatement", 'condition, if_block, else_block')
WhileStatement = recordtype("WhileStatement", 'condition, body')
BinaryExpression = recordtype('BinaryExpression', 'left, op, right')
IntConst = recordtype('IntConst', 'value')
Variable = recordtype('Variable', 'name')


# Assign the custom __repr__ functions to all nodes.
ClassDeclaration.repr = class_decl_repr
MethodDeclaration.repr = method_decl_repr
VarDeclaration.repr = var_decl_repr
Type.repr = type_repr
NewObject.repr = new_obj_repr
Assignment.repr = assignment_repr
ReturnStatement.repr = return_stmt_repr
MethodCall.repr = method_call_repr
IfStatement.repr = if_stmt_repr
WhileStatement.repr = while_stmt_repr
BinaryExpression.repr = binary_expr_repr
IntConst.repr = int_const_repr
Variable.repr = variable_repr
