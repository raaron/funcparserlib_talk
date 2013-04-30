#!/usr/bin/env python

from parser import Parser
from evaluator_visitor import EvaluatorVisitor


class Interpreter(object):
    """Interprets a javali program."""

    def __init__(self):
        self.parser = Parser()
        self.evaluator = EvaluatorVisitor()

    def interprete_file(self, filename):
        """
        Interpretes a javali program read from file with 'filename' if it
        is valid.
        """
        with open(filename, 'r') as f:
            return self.interprete_code(f.read())

    def interprete_code(self, code):
        """Interpretes javali 'code' if it is valid."""

        ast = self.parser.parse(code)
        return self.evaluator.evaluate(ast)

    def get_result(self):
        """Return the result of the evaluator."""

        return self.evaluator.result

    def print_output(self):
        """Print the output of the evaluator."""

        print '\n'.join(str(i) for i in self.get_result())


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.interprete_file("input.javali")
    interpreter.print_output()
