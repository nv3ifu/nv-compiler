from pyparsing import rest_of_line

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


class Identifier(Expr):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return f'Identifier[{self.name}]'


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


class Bool(Expr):
    def __init__(self, value, line):
        assert isinstance(value, bool), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Bool[{self.value}]'


class String(Expr):
    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line

    def __repr__(self):
        return f'String[{self.value}]'


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


class LogicalOp(Expr):

    def __init__(self, op: Token, left: Expr, right: Expr, line):
        assert isinstance(op, Token), op
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f'LogicalOp({self.op.lexeme!r},{self.left},{self.right})'


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


class WhileStmt(Stmt):
    pass


class Assignment(Stmt):
    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Assignment({self.name}, {self.value})'


class Stmts(Node):
    def __init__(self, stmts, line):
        assert all(isinstance(stmt, Stmt) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line

    def __repr__(self):
        return f'Stmts({self.stmts})'


class PrintStmt(Stmt):
    def __init__(self, value, line,end):
        assert isinstance(value, Expr), value
        self.value = value
        self.line = line
        self.end = end

    def __repr__(self):
        return f'PrintStmt({self.value},end = {self.end!r})'

class IfStmt(Stmt):

    def __init__(self,test,then_stmts,else_stmts,line):
        assert isinstance(test,Expr),test
        assert isinstance(then_stmts,Stmts),then_stmts
        assert isinstance(else_stmts,Stmts),else_stmts
        self.test = test
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
    def __repr__(self):
        return f'IfStmt(test:{self.test},then_stmts:{self.then_stmts},else_stmts{self.else_stmts})'
class ForStmt(Stmt):
    pass
