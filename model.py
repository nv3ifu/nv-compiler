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

class Decl(Stmt):
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
    def __init__(self,test,body_stmts,line):
        assert isinstance(test,Expr),test
        assert isinstance(body_stmts,Stmts),body_stmts
        self.test = test
        self.body_stmts = body_stmts
        self.line = line
    def __repr__(self):
        return f'WhileStmt({self.test},{self.body_stmts})'



class Assignment(Stmt):
    def __init__(self, left, right, line):
        assert isinstance(left, Expr), left
        assert isinstance(right, Expr), right
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return f'Assignment({self.left}, {self.right})'


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

    def __init__(self, test, then_stmts, else_stmts, line):
        assert isinstance(test, Expr), test
        assert isinstance(then_stmts, Stmts), then_stmts
        assert else_stmts is None or isinstance(else_stmts, Stmts), else_stmts
        self.test = test
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        self.line = line

    def __repr__(self):
        return f'IfStmt(test:{self.test},then_stmts:{self.then_stmts},else_stmts:{self.else_stmts})'


class ForStmt(Stmt):
    def __init__(self, ident, start, end, step, body_stmts, line):
        assert isinstance(ident, Identifier), ident
        assert isinstance(start, Expr), start
        assert isinstance(end, Expr), end
        assert step is None or isinstance(step, Expr), step
        assert isinstance(body_stmts, Stmts), body_stmts
        self.ident = ident
        self.start = start
        self.end = end
        self.step = step
        self.body_stmts = body_stmts
        self.line = line

    def __repr__(self):
        return f'ForStmt({self.ident},{self.start},{self.end},{self.step},{self.body_stmts})'

class FuncDecl(Decl):
    def __init__(self,name,params,body_stmts,line):
        assert isinstance(name,str),name
        assert all(isinstance(param,Params) for param in params) ,params
        self.name = name
        self.params = params
        self.body_stmts = body_stmts
        self.line = line
    def __repr__(self):
        return f'FuncDecl({self.name},{self.params},{self.body_stmts})'

class Params(Decl):
    def __init__(self,name,line):
        assert isinstance(name,str),name
        self.name = name
        self.line = line
    def __repr__(self):
        return f'Params({self.name})'

class FuncCall(Expr):
    def __init__(self,name,args,line):
        assert isinstance(name,str),name
        assert all(isinstance(arg,Expr) for arg in args),args
        self.name = name
        self.args = args
        self.line = line
    def __repr__(self):
        return f'FuncCall({self.name},{self.args})'

class FuncCallStmt(Stmt):
    def __init__(self,expr):
        assert isinstance(expr,Expr),expr
        self.expr = expr
    def __repr__(self):
        return f'FuncCallStmt({self.expr})'

class RetStmt(Stmt):
    def __init__(self,expr,line):
        assert isinstance(expr,Expr),expr
        self.expr = expr
        self.line = line
    def __repr__(self):
        return f'RetStmt({self.expr})'
    
class LocalStmt(Stmt):
    def __init__(self,ident,expr,line):
        assert isinstance(ident,str),ident
        assert isinstance(expr,Expr),expr
        self.ident = ident
        self.expr = expr
        self.line = line
    def __repr__(self):
        return f'LocalStmt({self.ident},{self.expr})'