from tokens import *


class Node:
    pass


class Stmt(Node):
    pass


class Expr(Node):
    """
    Example: x + ( 3 * y ) >= 6
    """
    pass


class Integer(Expr):
    def __init__(self, value, line):
        assert isinstance(value, int), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Integer[{self.value}]'


class Float(Expr):
    def __init__(self, value, line):
        assert isinstance(value, float), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Float[{self.value}]'


class Grouping(Expr):
    def __init__(self, value, line):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Grouping({self.value})'


class UnOp(Expr):
    """
    Example: -x
    """

    def __init__(self, op: Token, operand: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(operand, Expr), operand
        self.line = line
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'BinOp({self.op.lexeme!r},{self.operand})'


class BinOp(Expr):
    """
    Example: x + y
    """

    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f'BinOp({self.op.lexeme!r},{self.left},{self.right})'


def WhileStmt(Stmt):
    pass


def Assignment(Stmt):
    pass


def IfStmt(Stmt):
    pass


def ForStmt(Stmt):
    pass
