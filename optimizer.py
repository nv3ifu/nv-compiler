from model import *
from tokens import *

class ASTOptimizer:
    def optimize(self, node):
        if node is None:
            return None
        
        if isinstance(node, Integer):
            return node
        
        if isinstance(node, Float):
            return node
        
        if isinstance(node, Bool):
            return node
        
        if isinstance(node, String):
            return node
        
        if isinstance(node, Identifier):
            return node
        
        if isinstance(node, Grouping):
            node.value = self.optimize(node.value)
            if isinstance(node.value, (Integer, Float)):
                return node.value
            return node
        
        if isinstance(node, BinOp):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            return self.fold_binop(node)
        
        if isinstance(node, UnOp):
            node.operand = self.optimize(node.operand)
            return self.fold_unop(node)
        
        if isinstance(node, LogicalOp):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            return self.fold_logical(node)
        
        if isinstance(node, Assignment):
            node.right = self.optimize(node.right)
            return node
        
        if isinstance(node, PrintStmt):
            node.value = self.optimize(node.value)
            return node
        
        if isinstance(node, IfStmt):
            node.test = self.optimize(node.test)
            node.then_stmts = self.optimize(node.then_stmts)
            if node.else_stmts:
                node.else_stmts = self.optimize(node.else_stmts)
            return node
        
        if isinstance(node, WhileStmt):
            node.test = self.optimize(node.test)
            node.body_stmts = self.optimize(node.body_stmts)
            return node
        
        if isinstance(node, ForStmt):
            node.start = self.optimize(node.start)
            node.end = self.optimize(node.end)
            if node.step:
                node.step = self.optimize(node.step)
            node.body_stmts = self.optimize(node.body_stmts)
            return node
        
        if isinstance(node, FuncDecl):
            node.body_stmts = self.optimize(node.body_stmts)
            return node
        
        if isinstance(node, FuncCall):
            node.args = [self.optimize(arg) for arg in node.args]
            return node
        
        if isinstance(node, FuncCallStmt):
            node.expr = self.optimize(node.expr)
            return node
        
        if isinstance(node, RetStmt):
            node.expr = self.optimize(node.expr)
            return node
        
        if isinstance(node, LocalStmt):
            node.expr = self.optimize(node.expr)
            return node
        
        if isinstance(node, Stmts):
            node.stmts = [self.optimize(stmt) for stmt in node.stmts]
            return node
        
        return node
    
    def fold_binop(self, node):
        left = node.left
        right = node.right
        
        if not isinstance(left, (Integer, Float)) or not isinstance(right, (Integer, Float)):
            return node
        
        lval = left.value
        rval = right.value
        line = node.line
        
        op = node.op.token_type
        
        if op == TOK_PLUS:
            result = lval + rval
        elif op == TOK_MINUS:
            result = lval - rval
        elif op == TOK_STAR:
            result = lval * rval
        elif op == TOK_SLASH:
            if rval == 0:
                return node
            result = lval / rval
        elif op == TOK_CARET:
            result = lval ** rval
        elif op == TOK_MOD:
            if rval == 0:
                return node
            result = lval % rval
        elif op == TOK_GT:
            return Bool(lval > rval, line)
        elif op == TOK_GE:
            return Bool(lval >= rval, line)
        elif op == TOK_LT:
            return Bool(lval < rval, line)
        elif op == TOK_LE:
            return Bool(lval <= rval, line)
        elif op == TOK_EQEQ:
            return Bool(lval == rval, line)
        elif op == TOK_NE:
            return Bool(lval != rval, line)
        else:
            return node
        
        if isinstance(result, float) and result.is_integer():
            return Integer(int(result), line)
        elif isinstance(result, float):
            return Float(result, line)
        else:
            return Integer(result, line)
    
    def fold_unop(self, node):
        operand = node.operand
        
        if not isinstance(operand, (Integer, Float, Bool)):
            return node
        
        val = operand.value
        line = node.line
        op = node.op.token_type
        
        if op == TOK_MINUS:
            if isinstance(operand, Integer):
                return Integer(-val, line)
            elif isinstance(operand, Float):
                return Float(-val, line)
        elif op == TOK_PLUS:
            return operand
        elif op == TOK_NOT:
            if isinstance(operand, Bool):
                return Bool(not val, line)
        
        return node
    
    def fold_logical(self, node):
        left = node.left
        right = node.right
        
        if not isinstance(left, Bool) or not isinstance(right, Bool):
            return node
        
        line = node.line
        op = node.op.token_type
        
        if op == TOK_AND:
            return Bool(left.value and right.value, line)
        elif op == TOK_OR:
            return Bool(left.value or right.value, line)
        
        return node
