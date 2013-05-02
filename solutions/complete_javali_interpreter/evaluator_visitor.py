from base_visitor import BaseVisitor
from javali_ast import Type, MethodCall
import operator


class EvaluatorVisitor(BaseVisitor):
    """Evaluates a Javali program."""

    def __init__(self):
        super(EvaluatorVisitor, self).__init__()
        self.program = None

    def evaluate(self, program):
        """Main entry point to evaluate a program by calling Main.main()."""

        self.program = program
        self.visit(program)

    def visit_class_declaration(self, class_decl, arg=None):
        """If this is class Main(), then execute main()."""

        if class_decl.name == "Main":
            self.visit(MethodCall('main', []), Object(class_decl))

    def visit_binary_expression(self, binary_expr, this):
        """Evaluates a binary expression."""

        operators = {'+': operator.add,
                     '-': operator.sub,
                     '*': operator.mul,
                     '/': operator.div}

        left = self.visit(binary_expr.left, this)
        right = self.visit(binary_expr.right, this)
        op = operators[binary_expr.op]
        return op(left, right)

    def visit_int_const(self, int_const, this):
        """Return the value of the IntConst."""

        return int_const.value

    def visit_variable(self, variable, this):
        """Return the current value of this variable."""

        return this.get_value(variable.name)

    def visit_assignment(self, assignment, this):
        """
        Update the LHS of the assignment with the evaluated value of the RHS.
        """
        this.set_value(assignment.variable.name, self.visit(assignment.expr, this))

    def visit_return_statement(self, return_stmt, this):
        """
        Evaluate the expression and raise an exception holding the evaluated
        value.
        """
        raise ReturnStatementException(self.visit(return_stmt.expr, this))

    def visit_new_object(self, new_object, this):
        """Return a new object with the type of new_object."""

        return Object(self.program.class_mapping[new_object.type_.name])

    def visit_method_call(self, method_call, this):
        """Execute the method belonging to this method call."""

        if method_call.name == "write":
            print self.visit(method_call.parameters[0], this)
        else:
            parameter_values = self.visit_all(method_call.parameters, this)
            method_decl = this.method_mapping[method_call.name]

            old_parameter_mapping = this.parameter_mapping
            old_local_mapping = this.local_mapping

            this.setup_variable_mapping(method_decl, parameter_values)

            result = None

            try:
                self.visit_all(method_decl.stmts, this)
            except ReturnStatementException as e:
                result = e.return_value

            this.parameter_mapping = old_parameter_mapping
            this.local_mapping = old_local_mapping
            return result

    def visit_if_statement(self, if_stmt, this):
        """Execute the 'if' or the 'else' block depending on 'condition'."""

        condition = self.visit(if_stmt.condition)
        if condition:
            self.visit_all(if_stmt.if_block, this)
        else:
            self.visit_all(if_stmt.else_block, this)

    def visit_while_statement(self, while_stmt, this):
        """
        Executes the 'body' of the while loop as long as 'condition'
        evaluates to True.
        """
        condition = self.visit(while_stmt.condition, this)
        while condition:
            self.visit_all(while_stmt.body, this)
            condition = self.visit(while_stmt.condition, this)


class Object(object):
    """Class for all objects created by a Javali program."""

    def __init__(self, class_decl):
        self.class_decl = class_decl
        self.method_mapping = {m.name: m for m in self.class_decl.method_decls}
        self.field_mapping = {f.name: None for f in self.class_decl.fields}
        self.field_mapping['this'] = self
        self.parameter_mapping = {}
        self.local_mapping = {}

    def setup_variable_mapping(self, method_decl, parameter_values):
        """
        Update parameter_mapping to contain the values of the evaulated
        'parameter_values' and local_mapping to contain None for all locals.
        """
        self.parameter_mapping = {}
        for i in xrange(len(method_decl.parameters)):
            var_decl = method_decl.parameters[i]
            self.parameter_mapping[var_decl.name] = parameter_values[i]

        self.local_mapping = {l.name: None for l in method_decl.local_decls}

    def get_method(self, method_name):
        """Return the MethodDeclaration for this method."""

        return self.method_mapping[method_name]

    def get_value(self, variable_name):
        """Resolve the value of the variable with this 'variable_name'."""

        if variable_name in self.local_mapping:
            return self.local_mapping[variable_name]
        elif variable_name in self.parameter_mapping:
            return self.parameter_mapping[variable_name]
        elif variable_name in self.field_mapping:
            return self.field_mapping[variable_name]

    def set_value(self, variable_name, value):
        """
        Setting the value of the variable with this 'variable_name' to value.
        """
        if variable_name in self.local_mapping:
            self.local_mapping[variable_name] = value
        elif variable_name in self.parameter_mapping:
            self.parameter_mapping[variable_name] = value
        elif variable_name in self.field_mapping:
            self.field_mapping[variable_name] = value

    def __repr__(self):
        """Return a readable representation of the object and its fields."""

        result = "---------------\nJavali Object of type %s\n" % self.class_decl.name
        result += "\tFields:\n"
        for field_name, value in self.field_mapping.iteritems():
            if field_name != 'this':
                if isinstance(value, Object):
                    value = 'Javali Object of type %s' % value.class_decl.name

                result += "\t%s: %s\n" % (field_name, str(value))
        return result + '---------------'


class ReturnStatementException(Exception):
    """
    Exception to be thrown in case of an evaluated return statement.
    Stores the returned value.
    """
    def __init__(self, return_value):
        super(ReturnStatementException, self).__init__()
        self.return_value = return_value
