from model import LogicalOp
from model import *
from tokens import *
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL = 'TYPE_BOOL'  # true | false

class Symbol:
    def __init__(self,name):
        self.name = name

class Compiler:
    def __init__(self):
        self.code = []
        self.label_counter = 0
        self.globals =  []
        self.numglobals = 0

    def emit(self,op):
        self.code.append(op)

    def make_label(self):
        self.label_counter += 1
        return f'LABEL_{self.label_counter}'

    def get_symbol(self,name):
        for symbol in self.globals:
            if symbol.name == name:
                return symbol
        return None

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
            elif node.op.token_type == TOK_EQEQ:
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
                self.emit(('PUSH',(TYPE_BOOL,True)))
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

        if isinstance(node,Grouping):
            self.compile(node.value)

        if isinstance(node,IfStmt):
            self.compile(node.test)
            then_label = self.make_label()
            else_label = self.make_label()
            exit_label = self.make_label()
            self.emit(('JMPZ',else_label))
            self.emit(('LABEL',then_label))
            self.compile(node.then_stmts)
            self.emit(('JMP',exit_label))
            self.emit(('LABEL',else_label))
            if node.else_stmts:
                self.compile(node.else_stmts)
            self.emit(('LABEL',exit_label))

        if isinstance(node,Assignment):
            self.compile(node.right)
            symbol = self.get_symbol(node.left.name)
            if not symbol:
                new_symbol = Symbol(node.left.name)
                self.globals.append(new_symbol)
                self.numglobals += 1
                self.emit(('STORE_GLOBAL',new_symbol.name))
            else:
                self.emit(('STORE_GLOBAL',symbol.name))

        if isinstance(node,Identifier):
            symbol = self.get_symbol(node.name)
            if not symbol:
                compile_error(f"Undefined variable {node.name}",node.line)
            self.emit(('LOAD_GLOBAL',symbol.name))

    def compile_code(self,node):
        self.emit(('START',))
        self.compile(node)
        self.emit(('HALT',))
        return self.code
    


    

