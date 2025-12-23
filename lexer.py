from tokens import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []

    def advance(self):
        ch = self.source[self.curr]
        self.curr += 1
        return ch

    def add_token(self, token_type):
        self.tokens.append(Token(token_type,self.source[self.start:self.curr]))

    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            if ch == '+': self.add_token(TOK_PLUS)
            if ch == '-': self.add_token(TOK_MINUS)
            if ch == '*': self.add_token(TOK_STAR)
        return self.tokens




