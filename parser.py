from enum import Enum

class UnbalancedExpressionError(Exception):
    pass

class Parser:
    def __init__(self):
        self.expressions = []
        self.number = None
        self.operator = None

    def __call__(self, expression):
        if self.unbalanced_brackets(expression):
            raise UnbalancedExpressionError

        expression = expression.replace(" ", "") + " "

        for char in expression:
            self.collect_numbers(char)
            self.collect_operators(char)
            self.collect_brackets(char)

        self._convert_numbers()
        reduced_expression = Reducer(self.expressions).reduce()
        return Operation(reduced_expression).run()

    def unbalanced_brackets(self, expression):
        lb_count = expression.count("(")
        rb_count = expression.count(")")

        return lb_count != rb_count

    def collect_numbers(self, char):
        if char in Number.SUPPORTED_NUMERICS:
            if self.number is None:
                self.number = Number(char)
            elif self.number is not None:
                self.number.extend(char)

        elif self.number is not None:
            self.expressions.append(self.number)
            self.number = None

    def collect_operators(self, char):
        if char in Operation.SUPPORTED_OPERATORS:
            self.expressions.append(char)

    def collect_brackets(self, char):
        if char in BracketExpression.BRACKETS:
            self.expressions.append(char)

    def _convert_numbers(self):
        for index, expression in enumerate(self.expressions):
            if isinstance(expression, Number):
                self.expressions[index] = expression()

class Number:
    SUPPORTED_NUMERICS = [str(i) for i in range(10)]

    def __init__(self, char):
        self.number = char

    def extend(self, char):
        self.number += char

    def __call__(self):
        return int(self.number)

class Reducer:
    class State(Enum):
        OPENED = 0
        IN_PROGRESS = 1
        CLOSED = 2

    def __init__(self, unreduced_expression):
        self.unreduced_expression = unreduced_expression
        self.reduced_expression = None
        self.state = None

    def reduce(self):
        # no need to reduce if there are no brackets
        if self.unreduced_expression[0] != BracketExpression.OPEN:
            return self.unreduced_expression

        for term in self.unreduced_expression:
            self.capture_bracket_expressions(term)

        return self.reduced_expression()

    def capture_bracket_expressions(self, term):
        if term == BracketExpression.OPEN:
            self.reduced_expression = BracketExpression()
            self.state = self.State.OPENED

        elif self.state == self.State.OPENED and not self._closed(term):
            self.reduced_expression.root(term)
            self.state == self.State.IN_PROGRESS

        elif self.state == self.State.IN_PROGRESS and not self._closed(term):
            self.reduced_expression.append(term)

        elif self._closed(term):
            self.state = self.State.CLOSED

    def _closed(self, term):
        return term == BracketExpression.CLOSE

class BracketExpression:
    OPEN = "("
    CLOSE = ")"
    BRACKETS = [OPEN, CLOSE]

    def __init__(self):
        self.expression = []

    def root(self, root):
        self.expression.append(root)

    def append(self, term):
        self.expression.append(term)

    def __call__(self):
        return self.expression

class Operation:
    def __init__(self, arr_operation):
        self.lhs = arr_operation[0]
        self.operator = arr_operation[1]
        self.rhs = arr_operation[2]

    def run(self):
        return self.OPERATORS[self.operator](self.lhs, self.rhs)

    def add(a, b):
        return a + b

    def sub(a, b):
        return a - b

    def mult(a, b):
        return a * b

    def div(a, b):
        if b == 0:
            raise ZeroDivisionError

        return a / b

    OPERATORS = {
        "+": add,
        "-": sub,
        "*": mult,
        "/": div,
    }

    SUPPORTED_OPERATORS = list(OPERATORS.keys())
