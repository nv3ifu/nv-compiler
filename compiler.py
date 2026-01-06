from model import FuncCallStmt
from model import FuncDecl
from model import LogicalOp
from model import *
from tokens import *
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL = 'TYPE_BOOL'  # true | false

SYM_VAR = 'SYM_VAR'
SYM_FUNC = 'SYM_FUNC'

class Symbol:
    def __init__(self,name,symtype = SYM_VAR,depth = 0,arity = 0):
        self.name = name
        self.symtype = symtype
        self.depth = depth
        self.arity = arity

class Compiler:
    def __init__(self):
        self.code = []
        self.label_counter = 0
        self.globals =  []
        self.numglobals = 0
        self.locals = []
        self.functions = []
        self.scope_depth = 0


    def emit(self,op):
        self.code.append(op)

    def make_label(self):
        self.label_counter += 1
        return f'LABEL_{self.label_counter}'

    def begin_block(self):
        self.scope_depth += 1

    def end_block(self):
        self.scope_depth -= 1
        while len(self.locals) > 0 and self.locals[-1].depth > self.scope_depth:
            self.emit(('POP',))
            self.locals.pop()

    def get_func_symbol(self,name):
        for symbol in self.functions:
            if symbol.name == name:
                return symbol
        return None


    def get_var_symbol(self,name):
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i].name == name:
                return (self.locals[i], i)
        for i, symbol in enumerate(self.globals):
            if symbol.name == name:
                return (symbol, i)
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
            self.begin_block()
            self.compile(node.then_stmts)
            self.end_block()
            self.emit(('JMP',exit_label))
            self.emit(('LABEL',else_label))
            if node.else_stmts:
                self.begin_block()
                self.compile(node.else_stmts)
                self.end_block()
            self.emit(('LABEL',exit_label))

        if isinstance(node,WhileStmt):
            test_label = self.make_label()
            body_label = self.make_label()
            exit_label = self.make_label()
            self.emit(('LABEL',test_label))
            self.compile(node.test)
            self.emit(('JMPZ',exit_label))
            self.emit(('LABEL',body_label))
            self.begin_block()
            self.compile(node.body_stmts)
            self.end_block()
            self.emit(('JMP',test_label))
            self.emit(('LABEL',exit_label))


        if isinstance(node,Assignment):
            self.compile(node.right)
            symbol = self.get_var_symbol(node.left.name)
            if not symbol:
                new_symbol = Symbol(node.left.name,SYM_VAR,self.scope_depth)
                if self.scope_depth == 0:
                    self.globals.append(new_symbol)
                    self.emit(('STORE_GLOBAL',new_symbol.name))
                    self.numglobals += 1
                else:
                    self.emit(('STORE_LOCAL',len(self.locals)))
                    self.locals.append(new_symbol)
            else:
                sym,slot = symbol
                if sym.depth == 0:
                    self.emit(('STORE_GLOBAL',sym.name))
                else:
                    self.emit(('STORE_LOCAL',slot))

        if isinstance(node,Identifier):
            symbol = self.get_var_symbol(node.name)
            if not symbol:
                compile_error(f"Undefined variable {node.name}",node.line)
            sym,slot = symbol
            if sym.depth == 0:
                self.emit(('LOAD_GLOBAL',sym.name))
            else:
                self.emit(('LOAD_LOCAL',slot))

        if isinstance(node,LocalStmt):
            self.compile(node.expr)
            new_symbol = Symbol(node.ident,SYM_VAR,self.scope_depth)
            self.emit(('STORE_LOCAL',len(self.locals)))
            self.locals.append(new_symbol)
        
        if isinstance(node,FuncDecl):
            func = self.get_func_symbol(node.name)
            if func:
                end_label = self.make_label()
                self.emit(('JMP',end_label))
                self.emit(('LABEL',func.name))
                self.begin_block()
                for param in node.params:
                    new_symbol = Symbol(param.name,SYM_VAR,self.scope_depth)
                    self.locals.append(new_symbol)
                self.compile(node.body_stmts)
                self.end_block()
                self.emit(('PUSH',(TYPE_BOOL,False)))
                self.emit(('RET',))
                self.emit(('LABEL',end_label))


        if isinstance(node,FuncCall):
            func = self.get_func_symbol(node.name)
            if not func:
                compile_error(f"Undefined function {node.name}",node.line)
            if func.arity != len(node.args):
                compile_error(f"Function {node.name} expected {func.arity} arguments, got {len(node.args)}",node.line)
            for arg in node.args:
                self.compile(arg)
            self.emit(('CALL',func.name,len(node.args)))

        if isinstance(node,FuncCallStmt):
            self.compile(node.expr)
            self.emit(('POP',))

        if isinstance(node,RetStmt):
            if node.expr:
                self.compile(node.expr)
            else:
                self.emit(('PUSH',(TYPE_BOOL,False)))
            self.emit(('RET',))

    def collect_functions(self,node):
        if isinstance(node,Stmts):
            for stmt in node.stmts:
                self.collect_functions(stmt)
        elif isinstance(node,FuncDecl):
            if self.get_func_symbol(node.name) or self.get_var_symbol(node.name):
                compile_error(f"Function/Variable {node.name} already defined",node.line)
            new_func = Symbol(node.name,SYM_FUNC,0,len(node.params))
            self.functions.append(new_func)

    def collect_globals(self,node):
        if isinstance(node,Stmts):
            for stmt in node.stmts:
                self.collect_globals(stmt)
        elif isinstance(node,Assignment):

            if self.scope_depth == 0:
                name = node.left.name
                if not self.get_var_symbol(name) and not self.get_func_symbol(name):
                    new_symbol = Symbol(name, SYM_VAR, 0)
                    self.globals.append(new_symbol)

    def collect_symbols(self,node):
        self.collect_functions(node)
        self.collect_globals(node)

    def compile_code(self,node):
        self.collect_symbols(node)
        self.emit(('START',))
        self.compile(node)
        self.emit(('HALT',))
        return self.code
    


    

