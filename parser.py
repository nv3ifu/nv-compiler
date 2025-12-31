from model import *
from tokens import *
from utils import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def advance(self):
        token = self.tokens[self.curr]
        self.curr = self.curr + 1
        return token

    def peek(self):
        return self.tokens[self.curr]

    def is_next(self, expected_type):
        if self.curr >= len(self.tokens):
            return False
        return self.peek().token_type == expected_type

    def expect(self, expected_type):
        if self.curr >= len(self.tokens):
            parse_error('Unexpected end of input', self.previous_token().line)
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            parse_error(f'Expected {expected_type!r}, found {self.peek().lexeme!r}', self.peek().line)

    def previous_token(self):
        return self.tokens[self.curr - 1]

    def match(self, expected_type):
        if self.curr >= len(self.tokens):
            return False
        if self.peek().token_type != expected_type:
            return False
        self.curr = self.curr + 1
        return True

    def primary(self):
        if self.match(TOK_TRUE): return Bool(True, line=self.previous_token().line)
        if self.match(TOK_FALSE): return Bool(False, line=self.previous_token().line)
        if self.match(TOK_STRING): return String(str(self.previous_token().lexeme[1:-1]),
                                                 line=self.previous_token().line)
        if self.match(TOK_INTEGER): return Integer(int(self.previous_token().lexeme), line=self.previous_token().line)
        if self.match(TOK_FLOAT): return Float(float(self.previous_token().lexeme), line=self.previous_token().line)
        if self.match(TOK_IDENTIFIER):
            name_token = self.previous_token()
            if self.match(TOK_LPAREN):
                args = self.args()
                self.expect(TOK_RPAREN)
                return FuncCall(name_token.lexeme, args, name_token.line)
            else:
                return Identifier(name_token.lexeme, line=name_token.line)
        if self.match(TOK_LPAREN):
            expr = self.expr()
            if (not self.match(TOK_RPAREN)):
                parse_error('")" expected', self.previous_token().line)
            else:
                return Grouping(expr, line=self.previous_token().line)


    def exponent(self):
        expr = self.primary()
        if self.match(TOK_CARET):
            op = self.previous_token()
            right = self.exponent()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def unary(self):
        if self.match(TOK_NOT) or self.match(TOK_MINUS) or self.match(TOK_PLUS):
            op = self.previous_token()
            operand = self.unary()
            return UnOp(op, operand, line=op.line)
        return self.exponent()

    def modulo(self):
        expr = self.unary()
        while self.match(TOK_MOD):
            op = self.previous_token()
            right = self.unary()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def multiplication(self):
        expr = self.modulo()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match(TOK_GT) or self.match(TOK_GE) or self.match(TOK_LT) or self.match(TOK_LE):
            op = self.previous_token()
            right = self.addition()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TOK_EQEQ) or self.match(TOK_NE):
            op = self.previous_token()
            right = self.comparison()
            expr = BinOp(op, expr, right, line=op.line)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TOK_AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TOK_OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOp(op, expr, right, line=op.line)
        return expr

    def assignment(self):
        left = self.expr()
        if self.match(TOK_ASSIGN):
            op = self.previous_token()
            right = self.expr()
            if isinstance(left, Identifier):
                return Assignment(left, right, line=op.line)
            else:
                parse_error(f"Invalid assignment target {left}", op.line)
        return left

    def expr(self):
        return self.logical_or()

    def if_stmt(self):
        self.expect(TOK_IF)
        test = self.expr()
        self.expect(TOK_THEN)
        then_stmts = self.stmts()
        if self.is_next(TOK_ELSE):
            self.advance()
            else_stmts = self.stmts()
        else:
            else_stmts = None
        self.expect(TOK_END)
        return IfStmt(test,then_stmts,else_stmts,self.previous_token().line)


    def for_stmt(self):
        self.expect(TOK_FOR)
        identifier = self.primary()
        self.expect(TOK_ASSIGN)
        start = self.expr()
        self.expect(TOK_COMMA)
        end = self.expr()
        if self.is_next(TOK_COMMA):
            self.advance()
            step = self.expr()
        else:
            step = None
        self.expect(TOK_DO)
        body_stmts = self.stmts()
        self.expect(TOK_END)
        return ForStmt(identifier,start,end,step,body_stmts,self.previous_token().line)

    def while_stmt(self):
        self.expect(TOK_WHILE)
        test = self.expr()
        self.expect(TOK_DO)
        body_stmts = self.stmts()
        self.expect(TOK_END)
        return WhileStmt(test,body_stmts,self.previous_token().line)

    def print_stmt(self,end):
        if self.match(TOK_PRINT) or self.match(TOK_PRINTLN):
            val = self.expr()
            return PrintStmt(val,self.previous_token().line,end)

    def params(self):
        params = []
        count = 0
        while not self.is_next(TOK_RPAREN):
            count += 1
            if count > 255:
                parse_error('Too many parameters', self.previous_token().line)
            name = self.expect(TOK_IDENTIFIER)
            params.append(Params(name.lexeme,self.previous_token().line))
            if not self.is_next(TOK_RPAREN):
                self.expect(TOK_COMMA)
        return params

    def args(self):
        args = []
        while not self.is_next(TOK_RPAREN):
            arg = self.expr()
            args.append(arg)
            if not self.is_next(TOK_RPAREN):
                self.expect(TOK_COMMA)
        return args


    def func_decl(self):
        self.expect(TOK_FUNC)
        name = self.expect(TOK_IDENTIFIER)
        self.expect(TOK_LPAREN)
        params = self.params()
        self.expect(TOK_RPAREN)
        body_stmts = self.stmts()
        self.expect(TOK_END)
        return FuncDecl(name.lexeme,params,body_stmts,self.previous_token().line)

    def ret_stmt(self):
        self.expect(TOK_RET)
        expr = self.expr()
        return RetStmt(expr,self.previous_token().line)

    def stmt(self):
        if self.peek().token_type == TOK_PRINT:
            return self.print_stmt(end = '')
        if self.peek().token_type == TOK_PRINTLN:
            return self.print_stmt(end = '\n')
        if self.peek().token_type == TOK_IF:
            return self.if_stmt()
        if self.peek().token_type == TOK_WHILE:
            return self.while_stmt()
        if self.peek().token_type == TOK_FOR:
            return self.for_stmt()
        if self.peek().token_type == TOK_FUNC:
            return self.func_decl()
        if self.peek().token_type == TOK_RET:
            return self.ret_stmt()
        expr = self.expr()
        if self.match(TOK_ASSIGN):
            op = self.previous_token()
            right = self.expr()
            if isinstance(expr, Identifier):
                return Assignment(expr, right, line=op.line)
            else:
                parse_error(f"Invalid assignment target {expr}", op.line)
        return FuncCallStmt(expr)

    def stmts(self):
        stmts = []
        while self.curr < len(self.tokens):
            if self.peek().token_type in (TOK_ELSE, TOK_END):
                break
            stmt = self.stmt()
            stmts.append(stmt)
        return Stmts(stmts, self.previous_token().line)

    def program(self):
        stmts = self.stmts()
        return stmts

    def parse(self):
        ast = self.program()
        return ast
