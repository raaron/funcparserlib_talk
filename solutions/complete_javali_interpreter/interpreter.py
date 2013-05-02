from javali_parser import Parser
from evaluator_visitor import EvaluatorVisitor


class Interpreter(object):
    """Interprets a javali program."""

    def __init__(self):
        self.parser = Parser()
        self.evaluator = EvaluatorVisitor()

    def interprete(self, filename):
        """
        Interpretes a javali program read from file with 'filename' if it
        is valid.
        """
        with open(filename, 'r') as f:
            code = f.read()

        ast = self.parser.parse(code)
        self.evaluator.evaluate(ast)


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.interprete("input.javali")
