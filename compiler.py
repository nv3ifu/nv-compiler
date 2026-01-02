from model import LogicalOp
from model import *
from tokens import *
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL = 'TYPE_BOOL'  # true | false

class Compiler:
    def __init__(self):
        self.code = []

    def emit(self,op):
        self.code.append(op)

    def compile(self,node):
        if isinstance(node,Integer):
            value = (TYPE_NUMBER,float(node.value))
            self.emit(('PUSH',value))

        if isinstance(node,Float):
            value = (TYPE_NUMBER,float(node.value))
            self.emit(('PUSH',value))

        if isinstance(node,Bool):
            value = (TYPE_BOOL,True if node.value == 'true' or node.value == True else False)
            self.emit(('PUSH',value))

        if isinstance(node,String):
            value = (TYPE_STRING,stringify(node.value))
            self.emit(('PUSH',value))

        if isinstance(node,BinOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TOK_PLUS:
                self.emit(('ADD',))
            elif node.op.token_type == TOK_MINUS:
                self.emit(('SUB',))
            elif node.op.token_type == TOK_STAR:
                self.emit(('MUL',))
            elif node.op.token_type == TOK_SLASH:
                self.emit(('DIV',))
            elif node.op.token_type == TOK_CARET:
                self.emit(('EXP',))
            elif node.op.token_type == TOK_MOD:
                self.emit(('MOD',))
            elif node.op.token_type == TOK_EQ:
                self.emit(('EQ',))
            elif node.op.token_type == TOK_NE:
                self.emit(('NE',))
            elif node.op.token_type == TOK_GT:
                self.emit(('GT',))
            elif node.op.token_type == TOK_GE:
                self.emit(('GE',))
            elif node.op.token_type == TOK_LT:
                self.emit(('LT',))
            elif node.op.token_type == TOK_LE:
                self.emit(('LE',))

        if isinstance(node,UnOp):
            self.compile(node.operand)
            if node.op.token_type == TOK_PLUS:
                self.emit(('POS',))
            elif node.op.token_type == TOK_MINUS:
                self.emit(('NEG',))
            elif node.op.token_type == TOK_NOT:
                self.emit(('PUSH',(TYPE_NUMBER,1)))
                self.emit(('XOR',))

        if isinstance(node,LogicalOp):
            self.compile(node.left)
            self.compile(node.right)
            if node.op.token_type == TOK_AND:
                self.emit(('AND',))
            elif node.op.token_type == TOK_OR:
                self.emit(('OR',))


        if isinstance(node,Stmts):
            for stmt in node.stmts:
                self.compile(stmt)
        
        if isinstance(node,PrintStmt):
            self.compile(node.value)
            if node.end == '':
                self.emit(('PRINT',))
            else:
                self.emit(('PRINTLN',))

    def compile_code(self,node):
        self.emit(('START',))
        self.compile(node)
        self.emit(('HALT',))
        return self.code
